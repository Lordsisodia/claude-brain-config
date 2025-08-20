var y=Object.defineProperty,f=Object.defineProperties;var w=Object.getOwnPropertyDescriptors;var p=Object.getOwnPropertySymbols;var A=Object.prototype.hasOwnProperty,v=Object.prototype.propertyIsEnumerable;var m=(a,e,t)=>e in a?y(a,e,{enumerable:!0,configurable:!0,writable:!0,value:t}):a[e]=t,u=(a,e)=>{for(var t in e||(e={}))A.call(e,t)&&m(a,t,e[t]);if(p)for(var t of p(e))v.call(e,t)&&m(a,t,e[t]);return a},g=(a,e)=>f(a,w(e));var l=(a,e,t)=>new Promise((r,i)=>{var n=s=>{try{d(t.next(s))}catch(c){i(c)}},o=s=>{try{d(t.throw(s))}catch(c){i(c)}},d=s=>s.done?r(s.value):Promise.resolve(s.value).then(n,o);d((t=t.apply(a,e)).next())});import{s as h}from"./index-Blbobipf.js";const b="business-onboarding-data";function I(){try{const a=localStorage.getItem(b);return a?JSON.parse(a):null}catch(a){return console.error("Error retrieving business data:",a),null}}class S{generateUniqueId(){return Date.now().toString(36)+Math.random().toString(36).substr(2)}createInputFromOnboardingData(){const e=I();return e?{businessName:e.businessName,appPurpose:e.appPurpose,industry:e.industry,targetAudience:e.targetAudience,communicationPreference:e.communicationPreference}:null}generateResearchPrompt(e){return`
You are an expert market research analyst. Provide comprehensive industry research based on these requirements:

BUSINESS INFORMATION:
- Company: ${e.businessName}
- App Purpose: ${e.appPurpose}
- Industry: ${e.industry}
- Target Audience: ${e.targetAudience}

I need detailed research on this industry to inform an app development plan. Please provide:

1. Current industry trends and market direction
2. Key competitors and their app offerings
3. Target audience behaviors and preferences
4. Market growth projections
5. Technological factors impacting this industry
6. Specific recommendations for app development in this space
7. Opportunity areas that competitors might be missing
8. Challenges that need to be addressed

Focus on providing actionable insights that will directly inform app feature planning and technical decisions.
    `}generatePlanPrompt(e,t,r){return`
You are an expert app development consultant. Create a comprehensive app plan based on these requirements and research:

BUSINESS REQUIREMENTS:
- Company: ${e.businessName}
- App Purpose: ${e.appPurpose}
- Industry: ${e.industry}
- Target Audience: ${e.targetAudience}
- Budget: ${e.budget||"Not specified"}
- Timeline: ${e.timeline||"Flexible"}

INDUSTRY RESEARCH FINDINGS:
- Industry Trends: ${t.industryTrends.join(", ")}
- Key Competitors: ${t.keyCompetitors.join(", ")}
- User Behaviors: ${t.userBehaviors.join(", ")}
- Market Growth: ${t.marketGrowth}
- Tech Factors: ${t.technologicalFactors.join(", ")}
- Opportunity Areas: ${t.opportunityAreas.join(", ")}
- Challenges: ${t.challengesToAddress.join(", ")}

RECOMMENDATIONS FROM RESEARCH:
${t.recommendations.join(`
- `)}

ANALYSIS FOCUS: ${r.focusAreas.join(", ")}
DETAIL LEVEL: ${r.detailLevel}

Please provide a detailed analysis including:
1. Executive Summary
2. Recommended features with priorities (informed by the research)
3. Technical architecture recommendations
4. Development phases and timeline
5. Cost breakdown
6. UI/UX recommendations
7. Market analysis (leveraging the research provided)
8. Risk assessment and mitigation

Structure your response as a comprehensive app development plan that a client can understand and a development team can implement.
    `}callResearchAI(e,t){return l(this,null,function*(){console.log("🔍 Calling AI for industry research...");try{const{data:r,error:i}=yield h.functions.invoke("analyze-industry-research",{body:{businessData:{businessName:t.businessName,appPurpose:t.appPurpose,industry:t.industry,targetAudience:t.targetAudience}}});if(i)throw console.error("Supabase function error (research):",i),new Error(`Research AI generation failed: ${i.message}`);if(!r||!r.success)throw new Error("Research AI returned no data");return console.log("✅ Industry research generated successfully"),r.research}catch(r){return console.error("Error calling Research AI:",r),console.log("🔄 Falling back to mock research data..."),this.getMockResearchData(t)}})}callPlanAI(e,t,r,i){return l(this,null,function*(){console.log(`🤖 Calling AI model ${t} for app plan generation...`);try{const{data:n,error:o}=yield h.functions.invoke("generate-app-plan",{body:{businessData:{businessName:r.businessName,appPurpose:r.appPurpose,industry:r.industry,targetAudience:r.targetAudience,budget:r.budget,timeline:r.timeline},researchData:i,options:{model:t,includeMarketAnalysis:!0,includeCostEstimates:!0,detailLevel:"detailed"}}});if(o)throw console.error("Supabase function error (plan):",o),new Error(`App plan generation failed: ${o.message}`);if(!n||!n.success)throw new Error("App plan generation returned no data");return console.log("✅ AI app plan generated successfully"),n.rawResponse}catch(n){return console.error("Error calling Plan AI:",n),console.log("🔄 Falling back to enhanced mock response..."),this.getEnhancedMockResponse(r,i)}})}getMockResearchData(e){console.log("📊 Generating mock research data...");const t=e.industry.toLowerCase();return t.includes("e-commerce")||t.includes("retail")?{industryTrends:["Mobile-first shopping experiences","Sustainable and ethical product focus","AR product visualization","Social commerce integration","Personalized recommendations"],keyCompetitors:["Traditional retailers with omnichannel presence","Pure-play e-commerce platforms","Sustainable fashion marketplaces","Direct-to-consumer brands"],userBehaviors:["Researching product sustainability credentials","Seeking seamless mobile checkout","Expecting same-day/next-day delivery","Sharing purchases on social media","Demanding transparent supply chains"],marketGrowth:"Sustainable fashion sector growing at 8-10% annually, outpacing traditional retail",technologicalFactors:["Mobile payment adoption","AR/VR for virtual try-on","AI-powered personalization","Blockchain for supply chain transparency","Voice commerce emerging"],recommendations:["Prioritize mobile-first design with streamlined checkout","Implement sustainability filters and metrics","Include AR try-on capabilities for clothing","Build robust product recommendation engine","Develop social sharing capabilities"],opportunityAreas:["Carbon footprint tracking per purchase","Virtual styling assistance","Sustainability-focused loyalty program","Community features for sustainable fashion enthusiasts"],challengesToAddress:["Competitive market with established players","User skepticism about sustainability claims","Complex logistics for ethical supply chains","High customer acquisition costs"]}:t.includes("fitness")||t.includes("health")?{industryTrends:["Integration with wearable devices","Personalized workout and nutrition plans","Community and social fitness challenges","On-demand and live-streamed workouts","Gamification of fitness goals"],keyCompetitors:["Major fitness app platforms","Specialized workout apps","Wearable device companion apps","Nutrition and diet tracking apps"],userBehaviors:["Working out at home or on-the-go","Tracking progress across multiple metrics","Seeking community accountability","Personalizing fitness journeys","Integrating with existing devices"],marketGrowth:"Digital fitness market growing at 15% CAGR through 2027, accelerated by pandemic",technologicalFactors:["Wearable device proliferation","AI for workout form correction","Machine learning for personalization","Video streaming quality improvements","Battery optimization for all-day tracking"],recommendations:["Develop comprehensive device integration","Create AI-powered personalized plans","Build strong social and community features","Implement video-based workout library","Design gamified achievement system"],opportunityAreas:["Real-time form correction using device sensors","Hybrid home/gym workout planning","Mental wellness integration with physical fitness","Nutrition and workout correlation analysis"],challengesToAddress:["User retention beyond initial motivation period","Integration complexity with various devices","Creating engaging content consistently","Privacy concerns with health data"]}:t.includes("education")||t.includes("learning")?{industryTrends:["Microlearning and bite-sized content","Skills-based learning paths","Interactive coding environments","Certification and credential tracking","Peer-to-peer learning communities"],keyCompetitors:["MOOC platforms","Coding bootcamp apps","Language learning platforms","Professional development portals"],userBehaviors:["Learning in short, focused sessions","Practicing through interactive exercises","Seeking industry-relevant projects","Validating skills with certifications","Connecting with peers and mentors"],marketGrowth:"EdTech market growing at 16% annually, with professional skills segment growing faster",technologicalFactors:["Interactive coding environments in browser","AI-driven learning path optimization","Automated assessment technologies","Video conferencing and collaboration tools","Blockchain for credential verification"],recommendations:["Create structured learning paths with clear outcomes","Implement interactive coding exercises","Build progress tracking with visual metrics","Develop peer review and feedback systems","Offer shareable certificates and credentials"],opportunityAreas:["AI-powered personalized learning sequences","Mentor matching marketplace","Project-based assessments with real-world relevance","Community-driven content creation"],challengesToAddress:["High competition in the edtech space","Course completion and engagement rates","Keeping technical content up-to-date","Scaling personalized feedback"]}:{industryTrends:["Mobile-first user experiences","Personalization and AI-driven recommendations","Subscription-based business models","Integration with existing tools and platforms","Data privacy and security focus"],keyCompetitors:["Established players with legacy systems","Startup disruptors with modern technology","Adjacent industry players expanding their offerings","International competitors entering the market"],userBehaviors:["Increasing mobile usage for core tasks","Expecting seamless and intuitive experiences","Valuing time-saving automation features","Seeking personalized experiences","Looking for integration with existing workflows"],marketGrowth:`The ${e.industry} sector is growing steadily with digital transformation as a key driver`,technologicalFactors:["Cloud-based infrastructure adoption","AI and machine learning for personalization","API economy enabling integration ecosystems","Progressive web apps reducing friction","Data analytics driving decision-making"],recommendations:["Focus on intuitive mobile-first design","Implement personalization features early","Build with API-first architecture","Create seamless onboarding experience","Prioritize core user journeys"],opportunityAreas:["Workflow automation to save user time","Data visualization and insights","Cross-platform synchronization","Community and collaboration features"],challengesToAddress:["User adoption and habit formation","Technical complexity and maintenance","Security and compliance requirements","Differentiation in competitive market"]}}getEnhancedMockResponse(e,t){return`
# EXECUTIVE SUMMARY

Based on thorough industry research and analysis, we recommend developing a comprehensive ${e.appPurpose} solution for ${e.businessName} targeting ${e.targetAudience} in the ${e.industry} industry. Our research indicates key trends including ${t.industryTrends.slice(0,3).join(", ")}, which this app will address through innovative features and user experience.

# FEATURE RECOMMENDATIONS

## Core Features (High Priority)
- **User Authentication & Profiles**: Secure registration, login, and profile management
- **${e.appPurpose} Core Functions**: Main application functionality tailored to business needs
- **Product Management**: Comprehensive catalog with filtering and search capabilities
- **Shopping Experience**: Intuitive cart and checkout process

## Secondary Features (Medium Priority)  
- **Notifications System**: Real-time updates and promotional alerts
- **User Reviews & Ratings**: Community feedback and social proof
- **Wishlist Functionality**: Save and track desired items
- **Order Tracking**: Real-time status and delivery updates
- **Sustainability Features**: ${t.industryTrends.includes("Sustainable")?"Eco-friendly product filtering and carbon footprint tracking":"Features aligned with industry sustainability trends"}

## Advanced Features (Low Priority)
- **AR Capabilities**: ${t.technologicalFactors.includes("AR")?"Virtual try-on for products":"Advanced visualization features"}
- **Social Integration**: Sharing capabilities and community features
- **Loyalty Program**: Rewards and incentives for repeat customers

# TECHNICAL ARCHITECTURE

## Platform Recommendation
- **Approach**: Cross-platform development for iOS and Android
- **Framework**: React Native with TypeScript for code reusability
- **Backend**: Node.js with Express.js API

## Technology Stack
- **Frontend**: React Native, TypeScript, Redux
- **Backend**: Node.js, Express.js, JWT Authentication
- **Database**: PostgreSQL with Redis caching
- **Storage**: AWS S3 for file storage
- **Hosting**: AWS EC2 or Google Cloud Platform

# DEVELOPMENT PHASES

## Phase 1: Foundation (4-6 weeks)
- User authentication system
- Core app functionality
- Product catalog implementation
- Basic UI/UX implementation
- Database setup and API development

## Phase 2: E-commerce Functionality (3-4 weeks)
- Shopping cart functionality
- Checkout process
- Order tracking system
- Payment integration

## Phase 3: Enhancement (4-5 weeks)
- Notifications system
- Reviews functionality
- Wishlist implementation
- Sustainability features

## Phase 4: Advanced Features (4-6 weeks)
- AR capabilities implementation
- Social sharing integration
- Loyalty program development
- Final testing and optimization

# COST BREAKDOWN (GBP)

- **Development**: £28,000
- **UI/UX Design**: £8,000
- **Testing & QA**: £4,000
- **Deployment & Setup**: £2,000
- **First Year Maintenance**: £5,000
- **Total Project Cost**: £47,000

# MARKET ANALYSIS

The ${e.industry} industry shows strong growth potential with ${t.marketGrowth}. ${e.targetAudience} users are increasingly expecting ${t.userBehaviors[0]} and ${t.userBehaviors[1]}. Key competitors include ${t.keyCompetitors[0]} and ${t.keyCompetitors[1]}, but opportunity areas exist in ${t.opportunityAreas[0]} and ${t.opportunityAreas[1]}.

# RISKS AND MITIGATION

- **Technical Complexity**: Mitigate with experienced development team
- **Market Competition**: Focus on unique value proposition and user experience
- **Integration Challenges**: Implement thorough testing procedures
- **User Adoption**: Develop strong marketing strategy and intuitive onboarding
    `}parseAIResponse(e,t,r){const i=[{id:this.generateUniqueId(),name:"User Authentication",description:"Secure user registration, login, and profile management",priority:"high",complexity:"moderate",estimatedHours:40,dependencies:[],userStories:["As a user, I want to create an account so I can access the app","As a user, I want to securely log in to my account","As a user, I want to reset my password if I forget it","As a user, I want to update my profile information"]},{id:this.generateUniqueId(),name:"Core App Features",description:`Main functionality for ${t.appPurpose}`,priority:"high",complexity:"complex",estimatedHours:120,dependencies:[],userStories:[`As a user, I want to ${t.appPurpose.toLowerCase().includes("mobile")?"browse products on my mobile device":t.appPurpose.toLowerCase().includes("e-commerce")?"browse and purchase products":"access the core functionality"}`,"As a user, I want a mobile-first e-commerce platform for sustainable fashion and lifestyle products","As a user, I want to have a seamless browsing and shopping experience"]},{id:this.generateUniqueId(),name:"Product Management",description:"Comprehensive product catalog with filtering, searching, and recommendation engine",priority:"high",complexity:"moderate",estimatedHours:80,dependencies:[],userStories:["As a user, I want to search for products by category","As a user, I want to filter products by various attributes","As a user, I want to see recommended products based on my preferences","As a user, I want to view detailed product information and images"]},{id:this.generateUniqueId(),name:"Shopping Cart & Checkout",description:"Secure and intuitive shopping cart and checkout process with multiple payment options",priority:"high",complexity:"complex",estimatedHours:100,dependencies:[],userStories:["As a user, I want to add products to my cart","As a user, I want to modify quantities in my cart","As a user, I want to check out securely","As a user, I want to choose from multiple payment methods"]},{id:this.generateUniqueId(),name:"Notifications",description:"Push notifications and in-app messaging for order updates and promotions",priority:"medium",complexity:"moderate",estimatedHours:32,dependencies:[],userStories:["As a user, I want to receive notifications about important updates","As a user, I want to get alerts about order status changes","As a user, I want to receive personalized offers and promotions"]},{id:this.generateUniqueId(),name:"User Reviews & Ratings",description:"Allow users to leave reviews and ratings for products",priority:"medium",complexity:"simple",estimatedHours:24,dependencies:[],userStories:["As a user, I want to leave reviews for products I purchased","As a user, I want to rate products on a scale","As a user, I want to read other customers' reviews before making a purchase"]},{id:this.generateUniqueId(),name:"Wishlist",description:"Allow users to save products to a wishlist for future reference",priority:"medium",complexity:"simple",estimatedHours:16,dependencies:[],userStories:["As a user, I want to save products to my wishlist","As a user, I want to move items from my wishlist to my cart","As a user, I want to share my wishlist with friends"]},{id:this.generateUniqueId(),name:"Order Tracking",description:"Real-time order tracking and delivery status updates",priority:"medium",complexity:"moderate",estimatedHours:40,dependencies:[],userStories:["As a user, I want to track my order status in real-time","As a user, I want to receive delivery updates","As a user, I want to view my order history"]},{id:this.generateUniqueId(),name:"Sustainability Features",description:"Eco-friendly product filtering and carbon footprint tracking",priority:"medium",complexity:"complex",estimatedHours:60,dependencies:[],userStories:["As a user, I want to filter products by sustainability criteria","As a user, I want to see the carbon footprint of my purchases","As a user, I want to learn about sustainable practices"]},{id:this.generateUniqueId(),name:"AR Try-On",description:"Augmented reality feature for virtually trying on clothing items",priority:"low",complexity:"complex",estimatedHours:120,dependencies:[],userStories:["As a user, I want to virtually try on clothing items before purchasing","As a user, I want to see how items look on me from different angles","As a user, I want to share virtual try-on results with friends"]},{id:this.generateUniqueId(),name:"Social Sharing",description:"Allow users to share products and purchases on social media",priority:"low",complexity:"simple",estimatedHours:20,dependencies:[],userStories:["As a user, I want to share products on social media","As a user, I want to share my purchases with friends","As a user, I want to tag the brand in my social media posts"]},{id:this.generateUniqueId(),name:"Loyalty Program",description:"Rewards program with sustainability-focused incentives",priority:"low",complexity:"moderate",estimatedHours:50,dependencies:[],userStories:["As a user, I want to earn points for my purchases","As a user, I want to redeem points for rewards","As a user, I want to earn special rewards for eco-friendly choices"]}],n={platform:"cross-platform",techStack:{frontend:["React Native","TypeScript"],backend:["Node.js","Express"],database:["PostgreSQL","Redis"],apis:["REST API","WebSocket"]},architecture:"Microservices with API Gateway",scalability:"Horizontal scaling with load balancing",security:["JWT Authentication","HTTPS","Data Encryption"],integrations:["Payment Gateway","Push Notifications","Analytics",...r.technologicalFactors.slice(0,2)]},o=[{id:this.generateUniqueId(),name:"Phase 1: Foundation",description:"Core authentication and basic functionality",features:[i[0].id,i[1].id,i[2].id],estimatedDuration:"4-6 weeks",milestones:["User registration complete","Core features functional","Product catalog implemented"],deliverables:["MVP Backend","Basic UI/UX","Authentication System","Product Management"]},{id:this.generateUniqueId(),name:"Phase 2: E-commerce Functionality",description:"Shopping cart, checkout, and order management",features:[i[3].id,i[7].id],estimatedDuration:"3-4 weeks",milestones:["Shopping cart functionality","Checkout process","Order tracking system"],deliverables:["Complete Shopping Experience","Payment Integration","Order Management"]},{id:this.generateUniqueId(),name:"Phase 3: Enhancement",description:"Additional features and user engagement",features:[i[4].id,i[5].id,i[6].id,i[8].id],estimatedDuration:"4-5 weeks",milestones:["Notifications working","Reviews system","Wishlist functionality","Sustainability features"],deliverables:["Enhanced User Experience","Complete User Engagement Features"]},{id:this.generateUniqueId(),name:"Phase 4: Advanced Features",description:"AR try-on, social sharing, and loyalty program",features:[i[9].id,i[10].id,i[11].id],estimatedDuration:"4-6 weeks",milestones:["AR functionality","Social sharing integration","Loyalty program implementation"],deliverables:["Advanced Features","Final Testing","App Store Preparation"]}],d={development:28e3,design:8e3,testing:4e3,deployment:2e3,maintenance:5e3,total:47e3,currency:"GBP"},s={designSystem:"Modern Material Design with custom branding",colorScheme:`Professional palette suitable for ${t.industry}`,typography:"Clean, readable fonts optimized for mobile",userFlow:["Onboarding → Authentication → Product Browsing → Cart → Checkout → Order Tracking"],wireframes:["Welcome Screen","Login/Register","Product Catalog","Product Detail","Shopping Cart","Checkout","User Profile"],accessibility:["Screen reader support","High contrast mode","Large text options","Voice navigation"]};return{executiveSummary:`Based on thorough industry research and analysis of ${r.industryTrends.length} key trends, we recommend a comprehensive ${t.appPurpose} solution for ${t.businessName} targeting ${t.targetAudience} in the ${t.industry} industry.`,features:i,technicalRequirements:n,developmentPhases:o,costBreakdown:d,uiuxPlan:s,totalTimelineWeeks:20,mvpTimelineWeeks:10,recommendedMVPFeatures:[i[0].id,i[1].id,i[2].id,i[3].id,i[7].id],marketAnalysis:`The ${t.industry} industry shows ${r.marketGrowth}. Key trends include ${r.industryTrends.join(", ")}. Target users exhibit behaviors like ${r.userBehaviors.join(", ")}.`,competitorInsights:r.keyCompetitors,revenueModel:["Subscription model","In-app purchases","Premium features","Affiliate marketing"],risksAndMitigation:r.challengesToAddress.map(c=>`${c} - mitigated with ${this.getMitigationStrategy(c)}`)}}getMitigationStrategy(e){return e.toLowerCase().includes("competition")?"focused differentiation strategy and unique value proposition":e.toLowerCase().includes("technical")||e.toLowerCase().includes("complexity")?"experienced development team and phased approach":e.toLowerCase().includes("adoption")||e.toLowerCase().includes("retention")?"strong onboarding, user engagement features, and marketing strategy":e.toLowerCase().includes("integration")?"thorough testing and API-first architecture":e.toLowerCase().includes("privacy")||e.toLowerCase().includes("security")?"robust security measures and transparent privacy policies":"comprehensive planning and regular progress reviews"}generatePlan(r){return l(this,arguments,function*(e,t={model:"gpt-4",includeMarketAnalysis:!0,includeCostEstimates:!0,includeWireframes:!1,detailLevel:"detailed",focusAreas:["technical","business"]}){try{console.log("🚀 Starting multi-stage app plan generation process...");const i=this.generateResearchPrompt(e),n=yield this.callResearchAI(i,e);console.log("✅ Research phase complete with",n.industryTrends.length,"trends identified");const o=this.generatePlanPrompt(e,n,t),d=yield this.callPlanAI(o,t.model,e,n),s=this.parseAIResponse(d,e,n),c=u({id:this.generateUniqueId(),clientId:e.businessName.toLowerCase().replace(/\s+/g,"-"),businessName:e.businessName,generatedAt:new Date().toISOString(),modelUsed:t.model,version:"1.0",confidence:90,status:"draft"},s);return this.storePlan(c),console.log("🏁 Multi-stage app plan generation complete!"),c}catch(i){throw console.error("Error in multi-stage app plan generation:",i),new Error("Failed to generate app plan with research phase")}})}storePlan(e){try{const t=this.getAllStoredPlans();t.push(e),localStorage.setItem("generated-app-plans",JSON.stringify(t)),localStorage.setItem("latest-app-plan",JSON.stringify(e)),console.log("✅ App plan stored successfully:",e.id)}catch(t){console.error("Error storing app plan:",t)}}getStoredPlan(e){try{return this.getAllStoredPlans().find(r=>r.id===e)||null}catch(t){return console.error("Error retrieving plan:",t),null}}getAllStoredPlans(){try{const e=localStorage.getItem("generated-app-plans");return e?JSON.parse(e):[]}catch(e){return console.error("Error retrieving all plans:",e),[]}}getLatestPlan(){try{const e=localStorage.getItem("latest-app-plan");return e?JSON.parse(e):null}catch(e){return console.error("Error retrieving latest plan:",e),null}}refinePlan(e,t){return l(this,null,function*(){const r=this.getStoredPlan(e);if(!r)throw new Error("Plan not found");const i=g(u({},r),{id:this.generateUniqueId(),version:(parseFloat(r.version)+.1).toFixed(1),generatedAt:new Date().toISOString(),status:"draft"});return this.storePlan(i),i})}}const C=new S;export{C as a,I as g};
