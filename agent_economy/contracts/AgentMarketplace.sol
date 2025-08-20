// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/security/Pausable.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";

/**
 * @title AgentMarketplace
 * @dev A comprehensive marketplace for AI agent capabilities with token economics,
 *      bonding curves, reputation systems, and automated market making.
 *      
 *      Based on 2024-2025 research in agent economic models and DeFi mechanisms.
 */

contract AgentToken is ERC20, Ownable {
    using SafeMath for uint256;
    
    uint256 public constant MAX_SUPPLY = 1000000000 * 10**18; // 1 billion tokens
    uint256 public inflationRate = 500; // 5% per year (basis points)
    uint256 public lastInflationTime;
    
    mapping(address => bool) public minters;
    
    event InflationMinted(uint256 amount, uint256 timestamp);
    event MinterAdded(address minter);
    event MinterRemoved(address minter);
    
    constructor() ERC20("AgentToken", "AGENT") {
        _mint(msg.sender, 300000000 * 10**18); // Initial 30% circulation
        lastInflationTime = block.timestamp;
    }
    
    modifier onlyMinter() {
        require(minters[msg.sender], "Not authorized minter");
        _;
    }
    
    function addMinter(address _minter) external onlyOwner {
        minters[_minter] = true;
        emit MinterAdded(_minter);
    }
    
    function removeMinter(address _minter) external onlyOwner {
        minters[_minter] = false;
        emit MinterRemoved(_minter);
    }
    
    function mintInflation() external {
        require(block.timestamp >= lastInflationTime + 365 days, "Too early for inflation");
        
        uint256 inflationAmount = totalSupply().mul(inflationRate).div(10000);
        require(totalSupply().add(inflationAmount) <= MAX_SUPPLY, "Exceeds max supply");
        
        _mint(owner(), inflationAmount);
        lastInflationTime = block.timestamp;
        
        emit InflationMinted(inflationAmount, block.timestamp);
    }
    
    function mintReward(address to, uint256 amount) external onlyMinter {
        require(totalSupply().add(amount) <= MAX_SUPPLY, "Exceeds max supply");
        _mint(to, amount);
    }
    
    function burn(uint256 amount) external {
        _burn(msg.sender, amount);
    }
}

contract BondingCurve {
    using SafeMath for uint256;
    
    enum CurveType { LINEAR, EXPONENTIAL, POLYNOMIAL, BANCOR }
    
    struct CurveParams {
        CurveType curveType;
        uint256 basePrice;     // In wei
        uint256 slope;         // Slope parameter
        uint256 reserveRatio;  // For Bancor curves (in basis points)
    }
    
    CurveParams public params;
    uint256 public constant PRECISION = 1e18;
    
    constructor(
        CurveType _curveType,
        uint256 _basePrice,
        uint256 _slope,
        uint256 _reserveRatio
    ) {
        params = CurveParams(_curveType, _basePrice, _slope, _reserveRatio);
    }
    
    function calculatePrice(uint256 supply) public view returns (uint256) {
        if (params.curveType == CurveType.LINEAR) {
            return params.basePrice.add(params.slope.mul(supply).div(PRECISION));
        } else if (params.curveType == CurveType.POLYNOMIAL) {
            return params.basePrice.add(params.slope.mul(supply.mul(supply)).div(PRECISION.mul(PRECISION)));
        } else if (params.curveType == CurveType.BANCOR) {
            // Simplified Bancor: price = basePrice / (supply * reserveRatio + 1)
            uint256 denominator = supply.mul(params.reserveRatio).div(10000).add(PRECISION);
            return params.basePrice.mul(PRECISION).div(denominator);
        }
        
        return params.basePrice;
    }
    
    function calculateTokensForEth(uint256 ethAmount, uint256 currentSupply) 
        external view returns (uint256) {
        if (params.curveType == CurveType.LINEAR) {
            // Solve quadratic equation for linear bonding curve
            uint256 a = params.slope.div(2);
            uint256 b = params.basePrice.add(params.slope.mul(currentSupply).div(PRECISION));
            
            if (a == 0) {
                return ethAmount.mul(PRECISION).div(params.basePrice);
            }
            
            // Using quadratic formula: (-b + sqrt(b^2 + 4ac)) / 2a
            uint256 discriminant = b.mul(b).add(uint256(4).mul(a).mul(ethAmount));
            uint256 sqrtDiscriminant = sqrt(discriminant);
            
            if (sqrtDiscriminant <= b) return 0;
            
            return sqrtDiscriminant.sub(b).mul(PRECISION).div(uint256(2).mul(a));
        }
        
        // For other curves, use approximation
        return _approximateTokensForEth(ethAmount, currentSupply);
    }
    
    function _approximateTokensForEth(uint256 ethAmount, uint256 currentSupply) 
        internal view returns (uint256) {
        uint256 tokens = 0;
        uint256 stepSize = PRECISION.div(100); // 0.01 token steps
        uint256 totalCost = 0;
        
        for (uint256 i = 0; i < 1000; i++) { // Max 1000 iterations
            uint256 price = calculatePrice(currentSupply.add(tokens));
            uint256 stepCost = price.mul(stepSize).div(PRECISION);
            
            if (totalCost.add(stepCost) > ethAmount) break;
            
            totalCost = totalCost.add(stepCost);
            tokens = tokens.add(stepSize);
        }
        
        return tokens;
    }
    
    function sqrt(uint256 x) internal pure returns (uint256) {
        if (x == 0) return 0;
        uint256 z = x.add(1).div(2);
        uint256 y = x;
        while (z < y) {
            y = z;
            z = x.div(z).add(z).div(2);
        }
        return y;
    }
}

contract AgentMarketplace is ReentrancyGuard, Pausable, Ownable {
    using SafeMath for uint256;
    
    AgentToken public immutable agentToken;
    BondingCurve public immutable bondingCurve;
    
    enum AgentCapability { 
        REASONING, PLANNING, EXECUTION, ANALYSIS, 
        CREATIVITY, COORDINATION, LEARNING, COMMUNICATION 
    }
    
    struct Agent {
        address owner;
        AgentCapability[] capabilities;
        uint256 tokenBalance;
        uint256 stakedAmount;
        uint256 reputationScore; // Scaled by 1e18
        uint256 lastActiveTime;
        bool isActive;
        mapping(uint8 => uint256) performanceMetrics; // metric => score
        uint256 totalEarnings;
        uint256 completedJobs;
    }
    
    struct Job {
        uint256 id;
        address client;
        address assignedAgent;
        AgentCapability requiredCapability;
        uint256 payment;
        uint256 deadline;
        bool completed;
        bool paid;
        uint8 rating; // 1-5 stars
        string description;
    }
    
    struct Auction {
        uint256 jobId;
        uint256 startTime;
        uint256 endTime;
        address[] bidders;
        mapping(address => uint256) bids;
        address winner;
        uint256 winningBid;
        bool settled;
    }
    
    // State variables
    mapping(address => Agent) public agents;
    mapping(uint256 => Job) public jobs;
    mapping(uint256 => Auction) public auctions;
    mapping(AgentCapability => address[]) public capabilityProviders;
    mapping(AgentCapability => uint256) public capabilityDemand;
    
    uint256 public nextJobId = 1;
    uint256 public nextAuctionId = 1;
    uint256 public platformFeeRate = 500; // 5% in basis points
    uint256 public stakeRequirement = 1000 * 10**18; // 1000 tokens minimum stake
    uint256 public constant REPUTATION_SCALE = 1e18;
    uint256 public constant BANKRUPTCY_THRESHOLD = 10 * 10**18; // 10 tokens
    
    // Events
    event AgentRegistered(address indexed agent, AgentCapability[] capabilities, uint256 stake);
    event JobCreated(uint256 indexed jobId, address indexed client, AgentCapability capability, uint256 payment);
    event JobCompleted(uint256 indexed jobId, address indexed agent, uint8 rating);
    event AuctionStarted(uint256 indexed auctionId, uint256 indexed jobId, uint256 endTime);
    event BidPlaced(uint256 indexed auctionId, address indexed bidder, uint256 amount);
    event AuctionSettled(uint256 indexed auctionId, address indexed winner, uint256 winningBid);
    event ReputationUpdated(address indexed agent, uint256 newReputation);
    event AgentBankrupt(address indexed agent);
    event TokensPurchased(address indexed buyer, uint256 ethAmount, uint256 tokensReceived);
    
    constructor(address _agentToken, address _bondingCurve) {
        agentToken = AgentToken(_agentToken);
        bondingCurve = BondingCurve(_bondingCurve);
    }
    
    modifier onlyActiveAgent() {
        require(agents[msg.sender].isActive, "Agent not active");
        _;
    }
    
    modifier onlyAgentOwner(address agentAddr) {
        require(agents[agentAddr].owner == msg.sender, "Not agent owner");
        _;
    }
    
    // Agent registration and management
    function registerAgent(AgentCapability[] calldata capabilities) 
        external nonReentrant {
        require(capabilities.length > 0, "Must have at least one capability");
        require(!agents[msg.sender].isActive, "Agent already registered");
        require(agentToken.balanceOf(msg.sender) >= stakeRequirement, "Insufficient balance for stake");
        
        // Transfer stake
        agentToken.transferFrom(msg.sender, address(this), stakeRequirement);
        
        Agent storage agent = agents[msg.sender];
        agent.owner = msg.sender;
        agent.stakedAmount = stakeRequirement;
        agent.reputationScore = REPUTATION_SCALE; // Start with neutral reputation
        agent.lastActiveTime = block.timestamp;
        agent.isActive = true;
        
        // Store capabilities
        for (uint256 i = 0; i < capabilities.length; i++) {
            agent.capabilities.push(capabilities[i]);
            capabilityProviders[capabilities[i]].push(msg.sender);
        }
        
        emit AgentRegistered(msg.sender, capabilities, stakeRequirement);
    }
    
    function updatePerformanceMetrics(address agentAddr, uint8[] calldata metrics, uint256[] calldata scores) 
        external onlyOwner {
        require(metrics.length == scores.length, "Arrays length mismatch");
        
        Agent storage agent = agents[agentAddr];
        require(agent.isActive, "Agent not active");
        
        for (uint256 i = 0; i < metrics.length; i++) {
            agent.performanceMetrics[metrics[i]] = scores[i];
        }
        
        agent.lastActiveTime = block.timestamp;
    }
    
    // Job creation and management
    function createJob(
        AgentCapability capability, 
        uint256 payment, 
        uint256 deadline,
        string calldata description
    ) external nonReentrant {
        require(payment > 0, "Payment must be positive");
        require(deadline > block.timestamp, "Deadline must be in future");
        require(agentToken.balanceOf(msg.sender) >= payment, "Insufficient balance");
        
        // Transfer payment to escrow
        agentToken.transferFrom(msg.sender, address(this), payment);
        
        Job storage job = jobs[nextJobId];
        job.id = nextJobId;
        job.client = msg.sender;
        job.requiredCapability = capability;
        job.payment = payment;
        job.deadline = deadline;
        job.description = description;
        
        // Increase demand for this capability
        capabilityDemand[capability] = capabilityDemand[capability].add(1);
        
        emit JobCreated(nextJobId, msg.sender, capability, payment);
        nextJobId++;
    }
    
    function startAuction(uint256 jobId, uint256 duration) external {
        Job storage job = jobs[jobId];
        require(job.client == msg.sender, "Not job owner");
        require(!job.completed, "Job already completed");
        require(job.assignedAgent == address(0), "Job already assigned");
        
        Auction storage auction = auctions[nextAuctionId];
        auction.jobId = jobId;
        auction.startTime = block.timestamp;
        auction.endTime = block.timestamp.add(duration);
        
        emit AuctionStarted(nextAuctionId, jobId, auction.endTime);
        nextAuctionId++;
    }
    
    function placeBid(uint256 auctionId, uint256 bidAmount) 
        external onlyActiveAgent nonReentrant {
        Auction storage auction = auctions[auctionId];
        require(block.timestamp <= auction.endTime, "Auction ended");
        require(!auction.settled, "Auction already settled");
        require(bidAmount > 0, "Bid must be positive");
        
        Job storage job = jobs[auction.jobId];
        
        // Check if agent has required capability
        bool hasCapability = false;
        Agent storage agent = agents[msg.sender];
        for (uint256 i = 0; i < agent.capabilities.length; i++) {
            if (agent.capabilities[i] == job.requiredCapability) {
                hasCapability = true;
                break;
            }
        }
        require(hasCapability, "Agent lacks required capability");
        
        // Check if this is a new bidder
        if (auction.bids[msg.sender] == 0) {
            auction.bidders.push(msg.sender);
        }
        
        auction.bids[msg.sender] = bidAmount;
        
        emit BidPlaced(auctionId, msg.sender, bidAmount);
    }
    
    function settleAuction(uint256 auctionId) external nonReentrant {
        Auction storage auction = auctions[auctionId];
        require(block.timestamp > auction.endTime, "Auction still active");
        require(!auction.settled, "Auction already settled");
        
        // Find winning bid (lowest bid wins - reverse auction)
        address winner = address(0);
        uint256 winningBid = type(uint256).max;
        
        for (uint256 i = 0; i < auction.bidders.length; i++) {
            address bidder = auction.bidders[i];
            uint256 bid = auction.bids[bidder];
            
            if (bid < winningBid && bid > 0) {
                winningBid = bid;
                winner = bidder;
            }
        }
        
        if (winner != address(0)) {
            Job storage job = jobs[auction.jobId];
            job.assignedAgent = winner;
            auction.winner = winner;
            auction.winningBid = winningBid;
            
            emit AuctionSettled(auctionId, winner, winningBid);
        }
        
        auction.settled = true;
    }
    
    function completeJob(uint256 jobId, uint8 rating) external nonReentrant {
        Job storage job = jobs[jobId];
        require(job.client == msg.sender, "Not job client");
        require(job.assignedAgent != address(0), "No agent assigned");
        require(!job.completed, "Job already completed");
        require(rating >= 1 && rating <= 5, "Rating must be 1-5");
        
        job.completed = true;
        job.paid = true;
        job.rating = rating;
        
        // Calculate payment after platform fee
        uint256 platformFee = job.payment.mul(platformFeeRate).div(10000);
        uint256 agentPayment = job.payment.sub(platformFee);
        
        // Transfer payment to agent
        agentToken.transfer(job.assignedAgent, agentPayment);
        
        // Update agent stats
        Agent storage agent = agents[job.assignedAgent];
        agent.totalEarnings = agent.totalEarnings.add(agentPayment);
        agent.completedJobs = agent.completedJobs.add(1);
        agent.lastActiveTime = block.timestamp;
        
        // Update reputation based on rating
        _updateReputation(job.assignedAgent, rating);
        
        emit JobCompleted(jobId, job.assignedAgent, rating);
    }
    
    function _updateReputation(address agentAddr, uint8 rating) internal {
        Agent storage agent = agents[agentAddr];
        
        // Exponential moving average for reputation
        uint256 alpha = 300; // 3% learning rate (in basis points)
        uint256 ratingScore = uint256(rating).mul(REPUTATION_SCALE).div(5); // Convert 1-5 to 0-1e18
        
        uint256 newReputation = agent.reputationScore
            .mul(uint256(10000).sub(alpha))
            .add(ratingScore.mul(alpha))
            .div(10000);
        
        agent.reputationScore = newReputation;
        
        emit ReputationUpdated(agentAddr, newReputation);
    }
    
    // Token trading through bonding curve
    function purchaseTokens() external payable nonReentrant {
        require(msg.value > 0, "Must send ETH");
        
        uint256 currentSupply = agentToken.totalSupply();
        uint256 tokensToMint = bondingCurve.calculateTokensForEth(msg.value, currentSupply);
        
        require(tokensToMint > 0, "No tokens to mint");
        
        // Mint tokens to buyer
        agentToken.mintReward(msg.sender, tokensToMint);
        
        emit TokensPurchased(msg.sender, msg.value, tokensToMint);
    }
    
    // Economic pressure and natural selection
    function checkBankruptcy(address agentAddr) external {
        Agent storage agent = agents[agentAddr];
        require(agent.isActive, "Agent already inactive");
        
        uint256 totalAssets = agent.tokenBalance.add(agent.stakedAmount);
        bool lowReputation = agent.reputationScore < REPUTATION_SCALE.div(2); // Below 0.5
        bool inactive = block.timestamp > agent.lastActiveTime.add(30 days);
        
        if (totalAssets < BANKRUPTCY_THRESHOLD && (lowReputation || inactive)) {
            // Agent goes bankrupt
            agent.isActive = false;
            
            // Remove from capability providers
            for (uint256 i = 0; i < agent.capabilities.length; i++) {
                AgentCapability cap = agent.capabilities[i];
                address[] storage providers = capabilityProviders[cap];
                
                for (uint256 j = 0; j < providers.length; j++) {
                    if (providers[j] == agentAddr) {
                        providers[j] = providers[providers.length - 1];
                        providers.pop();
                        break;
                    }
                }
            }
            
            // Burn remaining staked tokens (economic punishment)
            if (agent.stakedAmount > 0) {
                agentToken.burn(agent.stakedAmount);
                agent.stakedAmount = 0;
            }
            
            emit AgentBankrupt(agentAddr);
        }
    }
    
    // Getters
    function getAgentCapabilities(address agentAddr) external view returns (AgentCapability[] memory) {
        return agents[agentAddr].capabilities;
    }
    
    function getCapabilityProviders(AgentCapability capability) external view returns (address[] memory) {
        return capabilityProviders[capability];
    }
    
    function getAuctionBidders(uint256 auctionId) external view returns (address[] memory) {
        return auctions[auctionId].bidders;
    }
    
    function getAuctionBid(uint256 auctionId, address bidder) external view returns (uint256) {
        return auctions[auctionId].bids[bidder];
    }
    
    function calculateCapabilityPrice(AgentCapability capability) external view returns (uint256) {
        uint256 providers = capabilityProviders[capability].length;
        uint256 demand = capabilityDemand[capability];
        
        if (providers == 0) return 0;
        
        // Base price influenced by supply and demand
        uint256 basePrice = 100 * 10**18; // 100 tokens base
        uint256 supplyDemandRatio = demand.mul(1e18).div(providers);
        
        return basePrice.add(basePrice.mul(supplyDemandRatio).div(1e18));
    }
    
    // Admin functions
    function setPlatformFeeRate(uint256 _feeRate) external onlyOwner {
        require(_feeRate <= 1000, "Fee rate too high"); // Max 10%
        platformFeeRate = _feeRate;
    }
    
    function setStakeRequirement(uint256 _requirement) external onlyOwner {
        stakeRequirement = _requirement;
    }
    
    function emergencyPause() external onlyOwner {
        _pause();
    }
    
    function emergencyUnpause() external onlyOwner {
        _unpause();
    }
    
    function withdrawFees() external onlyOwner {
        payable(owner()).transfer(address(this).balance);
    }
}