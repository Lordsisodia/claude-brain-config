var ee=Object.defineProperty,te=Object.defineProperties;var ae=Object.getOwnPropertyDescriptors;var H=Object.getOwnPropertySymbols;var re=Object.prototype.hasOwnProperty,se=Object.prototype.propertyIsEnumerable;var z=(h,t,r)=>t in h?ee(h,t,{enumerable:!0,configurable:!0,writable:!0,value:r}):h[t]=r,m=(h,t)=>{for(var r in t||(t={}))re.call(t,r)&&z(h,r,t[r]);if(H)for(var r of H(t))se.call(t,r)&&z(h,r,t[r]);return h},p=(h,t)=>te(h,ae(t));var v=(h,t,r)=>new Promise((s,a)=>{var o=y=>{try{d(r.next(y))}catch(A){a(A)}},x=y=>{try{d(r.throw(y))}catch(A){a(A)}},d=y=>y.done?s(y.value):Promise.resolve(y.value).then(o,x);d((r=r.apply(h,t)).next())});import{r as D,j as e,bT as w,H as I,dh as C,bf as ie,ah as V,bq as ne,cD as O,cA as L,fc as oe,eD as ce,bo as G,bn as le}from"./vendor-C50ijZWh.js";import{s as U,C as g,a as b,b as f,g as R,c as u,B as T,I as S,d as N,E as j}from"./index-Blbobipf.js";import{T as _,a as q,b as k,c as P}from"./tabs-CsM4ZGNr.js";import de from"./AppPlanTestingDashboard-CJd19M79.js";import{T as B}from"./textarea-B56zo4Tx.js";import{S as me}from"./separator-BNrJR0ZO.js";import"./libs-B3eAAgHd.js";import"./supabase-D8k0GRjn.js";import"./scroll-area-D4x0YgaW.js";import"./alert-y6vZCamD.js";class pe{generateInitialResearchPrompt(t){return`You are an expert market researcher conducting the INITIAL PHASE of research for an app development project. Your goal is to provide a comprehensive overview that will serve as the foundation for deeper research in the next phase.

**OBJECTIVE**: Conduct broad market research to understand the competitive landscape, industry trends, and market opportunities for ${t.companyName} in the ${t.industry} sector.

**Company Information**:
- **Company Name**: ${t.companyName}
- **Industry**: ${t.industry}
- **Location**: ${t.location}
- **Products/Services**: ${t.productsServices}
- **Target Users**: ${t.targetUsers}

**Research Requirements**:

1. **Industry Overview** - Provide market size, key trends, and growth drivers
2. **Competitor Landscape** - Identify 5-8 direct and indirect competitors
3. **Market Opportunities** - Identify gaps and technology trends
4. **Location Analysis** - Local market dynamics and consumer behavior

**Output Format**: Structure as Notion-ready markdown with callout boxes (use > ℹ️ format).

# 🔍 Initial Research Report for ${t.companyName}

**Note**: Copy and paste this report into Notion. For callout boxes (marked with > and an emoji), select the block and type \`/callout\` to convert.

---

## 📊 Industry Overview
> 📈 **Market Context**: Understanding the ${t.industry} landscape  
- **Market Size**: [Current market size and projections]  
- **Key Trends**: [3-4 major industry trends]  
- **Growth Drivers**: [What's driving market growth]  
- **Market Maturity**: [Is this a mature or emerging market?]

---

## 🏪 Competitor Landscape
### Direct Competitors
> 🎯 **Direct Competition**: Companies offering similar products/services  
- **[Competitor 1]**: [Brief description and key differentiators]  
- **[Competitor 2]**: [Brief description and key differentiators]  
- **[Competitor 3]**: [Brief description and key differentiators]

### Indirect Competitors
> 🔄 **Indirect Competition**: Alternative solutions customers might choose  
- **[Alternative 1]**: [How it competes indirectly]  
- **[Alternative 2]**: [How it competes indirectly]

---

## 💡 Market Opportunities
> 🚀 **Identified Gaps**: Potential areas for differentiation  
- **Gap 1**: [Market gap and opportunity]  
- **Gap 2**: [Market gap and opportunity]  
- **Technology Trends**: [Relevant tech trends to leverage]  
- **Target Market Insights**: [Key insights about target users]

---

## 🌍 Location Analysis (${t.location})
> 📍 **Local Market Dynamics**:  
- **Regional Competitors**: [Key local players]  
- **Consumer Behavior**: [Local preferences and habits]  
- **Market Penetration**: [How saturated is the local market?]  
- **Opportunities**: [Location-specific advantages]

---

## 🔚 Next Steps for Deeper Research
- **Detailed Feature Analysis**: Deep dive into competitor app features  
- **User Experience Review**: Analyze competitor UX/UI strategies  
- **Pricing Research**: Understand pricing models and strategies  
- **Customer Feedback Analysis**: Review user reviews and feedback  

---`}generateRefinedResearchPrompt(t,r){return`You are an expert market researcher conducting the REFINED RESEARCH PHASE. Using the initial research findings, conduct a deeper analysis to inform app development strategy.

**CONTEXT FROM INITIAL RESEARCH**:
Based on the initial research for ${r.companyName}, we identified:
- **Key Competitors**: ${r.competitorLandscape.directCompetitors.map(s=>s.name).join(", ")}
- **Market Opportunities**: ${r.marketOpportunities.identifiedGaps.join(", ")}
- **Industry Trends**: ${r.industryOverview.keyTrends.join(", ")}

**REFINED RESEARCH OBJECTIVES**:
1. **Detailed Competitor Analysis** - Feature matrices, pricing, UX comparison
2. **Deep Market Analysis** - Validate opportunities, assess risks, size markets
3. **Strategic Recommendations** - Differentiation strategy and feature priorities
4. **Technical Considerations** - Integration requirements and platform decisions

**Output Format**: Notion-ready markdown with detailed analysis tables and callout boxes.

# 🎯 Refined Research Report for ${t.companyName}

**Note**: Copy and paste this report into Notion. For callout boxes (marked with > and an emoji), select the block and type \`/callout\` to convert.

---

## 🔬 Detailed Competitor Analysis

### Feature Matrix
> 📊 **Comprehensive Feature Comparison**:  

| Feature | ${r.competitorLandscape.directCompetitors.slice(0,4).map(s=>s.name).join(" | ")} |
|---------|${r.competitorLandscape.directCompetitors.slice(0,4).map(()=>"-------").join("|")}|
| Mobile App | [Yes/No for each] |
| Online Ordering | [Yes/No for each] |
| Loyalty Program | [Yes/No for each] |
| Payment Integration | [Yes/No for each] |
| User Accounts | [Yes/No for each] |

### Pricing Analysis
> 💰 **Market Pricing Insights**:  
- **Average Price Range**: [Price range analysis]  
- **Pricing Models**: [Subscription, one-time, freemium, etc.]  
- **Premium Features**: [What features command premium pricing]  
- **Value Perception**: [How customers perceive value]

### User Experience Comparison
> 🎨 **UX/UI Analysis**:  
- **[Competitor 1]**: Strengths: [list] | Weaknesses: [list] | User Rating: [rating]  
- **[Competitor 2]**: Strengths: [list] | Weaknesses: [list] | User Rating: [rating]  
- **[Competitor 3]**: Strengths: [list] | Weaknesses: [list] | User Rating: [rating]

---

## 📈 Deep Market Analysis

### Validated Opportunities
> ✅ **Evidence-Based Opportunities**:  
1. **[Opportunity 1]**: Market Evidence: [data] | Impact: [High/Medium/Low] | Complexity: [rating]  
2. **[Opportunity 2]**: Market Evidence: [data] | Impact: [High/Medium/Low] | Complexity: [rating]  
3. **[Opportunity 3]**: Market Evidence: [data] | Impact: [High/Medium/Low] | Complexity: [rating]

### Risk Assessment
> ⚠️ **Market Risks**:  
- **[Risk 1]**: Likelihood: [High/Medium/Low] | Impact: [description] | Mitigation: [strategy]  
- **[Risk 2]**: Likelihood: [High/Medium/Low] | Impact: [description] | Mitigation: [strategy]

### Market Sizing
> 📊 **Market Size Analysis**:  
- **TAM (Total Addressable Market)**: [size and description]  
- **SAM (Serviceable Addressable Market)**: [size and description]  
- **SOM (Serviceable Obtainable Market)**: [realistic capture estimate]

### Customer Personas
> 👥 **Target User Profiles**:  
- **Primary Persona**: [Demographics, needs, pain points, preferred features]  
- **Secondary Persona**: [Demographics, needs, pain points, preferred features]

---

## 🎯 Strategic Recommendations

### Differentiation Strategy
> 🌟 **Competitive Advantage**:  
[Detailed strategy for standing out in the market]

### Feature Priorities
> 🏆 **Development Roadmap**:  
- **High Priority**: [Feature] - Rationale: [why] - Differentiator: [Yes/No]  
- **Medium Priority**: [Feature] - Rationale: [why] - Differentiator: [Yes/No]  
- **Low Priority**: [Feature] - Rationale: [why] - Differentiator: [Yes/No]

### Market Entry Strategy
> 🚀 **Go-to-Market Approach**:  
[Strategy for entering the market and acquiring users]

---

## 🔧 Technical Considerations

### Required Integrations
> 🔌 **System Requirements**:  
- **Payment Processing**: [Requirements and recommendations]  
- **Third-party APIs**: [Necessary integrations]  
- **Analytics**: [Tracking and measurement needs]

### Platform Considerations
> 📱 **Technology Decisions**:  
- **Mobile Strategy**: [Native, hybrid, web app recommendations]  
- **Backend Requirements**: [Database, hosting, scaling needs]  
- **Security Considerations**: [Data protection, compliance needs]

---

## 🔚 Ready for App Plan Development
This refined research provides the strategic foundation for creating a comprehensive app development plan with evidence-based feature recommendations and competitive positioning.

---`}generateAppPlanPrompt(t,r){return`You are an expert app development planner creating a CLIENT-FACING app development plan. This plan will be delivered directly to the client and must be professional, comprehensive, and actionable.

${r?`
**RESEARCH INSIGHTS FROM REFINED ANALYSIS**:
Based on comprehensive research including:
- **Validated Opportunities**: ${r.deepMarketAnalysis.validatedOpportunities.map(a=>a.opportunity).join(", ")}
- **Strategic Differentiation**: ${r.strategicRecommendations.differentiationStrategy}
- **High Priority Features**: ${r.strategicRecommendations.featurePriorities.filter(a=>a.priority==="High").map(a=>a.feature).join(", ")}
- **Technical Requirements**: ${r.technicalConsiderations.requiredIntegrations.join(", ")}
- **Market Entry Strategy**: ${r.strategicRecommendations.marketEntryStrategy}
`:""}

**IMPORTANT**: This plan is informed by comprehensive market research and competitor analysis, ensuring evidence-based recommendations and strategic positioning.

The development process is accelerated:
- **Discovery & Feature Confirmation**: 2-3 days
- **Design**: 5 days
- **MVP Development**: 7 days (includes wireframes and basic functionality)
- **Review Call**: 1 day
- **Full Development**: 14 days
- **Launch**: 1 day

The technology stack includes:
- **Hosting**: Self-hosted
- **Code Management**: GitHub
- **Database**: Supabase

The budget estimate ranges from $500 to $2,500. Include a callout box emphasizing that the budget is flexible and can be adjusted by modifying the scope or features to meet the client's needs.

**User Input**:
- Company Name: ${t.businessName}
- Industry: ${t.industry}
- App Purpose: ${t.appPurpose}
- Target Users: ${t.targetAudience}
- Budget: ${t.budget||"$500-$2,500"}
- Timeline: ${t.timeline||"30 days"}

**Output Format**:
# 📱 App Development Plan for ${t.businessName}

**Note**: Copy and paste this plan into Notion. For callout boxes (marked with > and an emoji), select the block and type \`/callout\` to convert.

> 🔬 **Research-Backed Plan**: This development plan is based on comprehensive market research and competitor analysis to ensure strategic positioning and evidence-based feature recommendations.

---

## 📱 App Overview
> ℹ️ **Purpose**: ${t.appPurpose}  
- **Company**: ${t.businessName}  
- **Industry**: ${t.industry}  
- **Objective**: [Summarize the app's strategic goal based on research]  
- **Problem Solved**: [Describe the validated market need]  
- **Competitive Advantage**: [Key differentiators identified through research]

---

## 👥 Target Audience
> 🎯 **Research-Validated Users**: ${t.targetAudience}  
- **Primary Users**: [Detailed persona based on research]  
- **User Needs**:  
  - [Research-validated need 1]  
  - [Research-validated need 2]  
  - [Research-validated need 3]  
- **Key Benefits**:  
  - [Evidence-based benefit 1]  
  - [Evidence-based benefit 2]  
  - [Evidence-based benefit 3]

---

## ✨ Key Features
> 🏆 **Evidence-Based Feature Set**: Features prioritized based on competitor analysis and market research

### Essential Features (MVP)
- **[High Priority Feature 1]**: [Description with competitive rationale]  
- **[High Priority Feature 2]**: [Description with competitive rationale]  
- **[High Priority Feature 3]**: [Description with competitive rationale]

### Additional Add-ons (Phase 2)
- **[Medium Priority Feature 1]**: [Description and strategic value]  
- **[Medium Priority Feature 2]**: [Description and strategic value]  
- **[Enhancement Feature]**: [Future enhancement opportunity]

> 🔑 **Feature Prioritization**: Essential features form the MVP foundation based on competitive analysis. Add-ons provide differentiation opportunities and can be implemented in future phases based on user feedback and budget.

---

## 🏆 Competitive Analysis
> 🔍 **Market Position**: Based on comprehensive competitor research  
- **Key Competitors**: [Research-identified competitors]  
- **Our Differentiation**: [Strategic advantages from research]  
- **Market Opportunity**: [Validated market gaps we're addressing]  
- **Competitive Moat**: [How we maintain advantage]

---

## 💼 Benefits to the Business
> 💰 **Strategic Value Delivery**:  
- **Revenue Growth**: [Specific revenue opportunities identified]  
- **Market Position**: [Competitive positioning advantages]  
- **Customer Engagement**: [Engagement enhancement strategies]  
- **Operational Efficiency**: [Process improvement benefits]  
- **Future Scalability**: [Growth and expansion opportunities]

---

## 🚀 Development Process
> 🚀 **Proven Methodology**:  
1. **Discovery & Research Validation** (2-3 days)  
   - Confirm research findings with stakeholders  
   - Finalize feature specifications  
   - Validate technical requirements  

2. **Strategic Design** (5 days)  
   - Create wireframes based on competitive insights  
   - Design user experience flows  
   - Develop visual identity aligned with positioning  

3. **MVP Development** (7 days)  
   - Build core functionality  
   - Implement essential features  
   - Create working prototype  

4. **Stakeholder Review** (1 day)  
   - Present MVP for feedback  
   - Gather input and refinements  
   - Plan final development phase  

5. **Full Development** (14 days)  
   - Complete all planned features  
   - Implement additional functionality  
   - Conduct thorough testing  

6. **Launch & Deployment** (1 day)  
   - Final testing and optimization  
   - Deploy to production  
   - Launch preparation and monitoring

---

## ⏳ Timeline
> ⏰ **Estimated Duration**: ~30 days total  
- **Phase 1**: Discovery & Design (7-8 days)  
- **Phase 2**: Development & Testing (22-23 days)  
- **Note**: Timeline assumes standard complexity; sophisticated features may extend development time

---

## 💰 Budget Estimate
> 💡 **Flexible Investment**: Budget can be adjusted based on feature scope and priorities  
- **Estimated Range**: ${t.budget||"$500-$2,500"}  
- **Payment Structure**: Milestone-based payments aligned with development phases  
- **Scope Flexibility**: Features can be prioritized or deferred to meet budget constraints  
- **Value Optimization**: Research insights ensure maximum ROI from development investment

---

## 🔧 Technical Stack
> ⚙️ **Modern, Scalable Architecture**:  
- **Hosting**: Self-hosted for full control and customization  
- **Code Management**: GitHub for version control and collaboration  
- **Database**: Supabase for real-time data and authentication  
- **Frontend**: React with TypeScript for robust user interfaces  
- **Deployment**: Automated CI/CD for reliable updates

---

## 👉 Next Steps
> 🎯 **Project Initiation**:  
1. **Client Review**: Review this plan and provide feedback  
2. **Kickoff Meeting**: Schedule discovery session to begin project  
3. **Research Validation**: Confirm market insights with your team  
4. **Development Start**: Begin Phase 1 upon agreement  
5. **Ongoing Collaboration**: Regular check-ins throughout development

---

## 📞 Ready to Begin?
This research-backed plan provides a strategic foundation for your app development. The comprehensive market analysis ensures we're building features that matter to your users and differentiate you from competitors.

**Contact us to start your project**: [Contact information]

---`}executeThreeStageWorkflow(t,r,s){return v(this,null,function*(){try{s&&s("initial-research",15,"Conducting initial market research...");const a=yield this.executeInitialResearch(t);s&&s("refined-research",50,"Performing detailed analysis and validation...");const o=yield this.executeRefinedResearch(t,a);s&&s("app-plan",85,"Generating comprehensive app development plan...");const x=yield this.executeAppPlan(r,void 0,o);return s&&s("complete",100,"Three-stage process complete!"),{initialResearch:a,refinedResearch:o,appPlan:x}}catch(a){throw console.error("Three-stage workflow error:",a),new Error(`Three-stage workflow failed: ${a instanceof Error?a.message:"Unknown error"}`)}})}executeInitialResearch(t){return v(this,null,function*(){const r=this.generateInitialResearchPrompt(t);try{const{data:s,error:a}=yield U.functions.invoke("generate-app-plan",{body:{businessData:{businessName:t.companyName,industry:t.industry,targetAudience:t.targetUsers,appPurpose:`Initial research for ${t.productsServices}`,location:t.location},options:{customPrompt:r,isInitialResearchPhase:!0,model:"gemini-2.0-flash"}}});if(a)throw new Error(a.message||"Initial research generation failed");const o=this.parseInitialResearchResponse(s.rawResponse,t);return yield this.storeInitialResearchReport(o),o}catch(s){throw console.error("Initial research execution error:",s),s}})}executeRefinedResearch(t,r){return v(this,null,function*(){const s=this.generateRefinedResearchPrompt(t,r);try{const{data:a,error:o}=yield U.functions.invoke("generate-app-plan",{body:{businessData:{businessName:t.companyName,industry:t.industry,targetAudience:t.targetUsers,appPurpose:`Refined research for ${t.productsServices}`,location:t.location},options:{customPrompt:s,isRefinedResearchPhase:!0,model:"gemini-2.0-flash",includeInitialResearch:!0,initialResearchData:r}}});if(o)throw new Error(o.message||"Refined research generation failed");const x=this.parseRefinedResearchResponse(a.rawResponse,t,r);return yield this.storeRefinedResearchReport(x),x}catch(a){throw console.error("Refined research execution error:",a),a}})}executeAppPlan(t,r,s){return v(this,null,function*(){const a=this.generateAppPlanPrompt(t,s);try{const{data:o,error:x}=yield U.functions.invoke("generate-app-plan",{body:{businessData:{businessName:t.businessName,appPurpose:t.appPurpose,industry:t.industry,targetAudience:t.targetAudience,budget:t.budget,timeline:t.timeline},options:{customPrompt:a,isAppPlanPhase:!0,model:"gemini-2.0-flash",includeRefinedResearch:!!s,refinedResearchData:s}}});if(x)throw new Error(x.message||"App plan generation failed");const d=this.parseAppPlanResponse(o.rawResponse,t,s==null?void 0:s.id);return yield this.storeAppPlan(d),d}catch(o){throw console.error("App plan execution error:",o),o}})}parseInitialResearchResponse(t,r){return{id:`initial_research_${Date.now()}`,companyName:r.companyName,generatedAt:new Date().toISOString(),industryOverview:{marketSize:this.extractSectionText(t,"Market Size"),keyTrends:this.extractListFromSection(t,"Key Trends"),growthDrivers:this.extractListFromSection(t,"Growth Drivers")},competitorLandscape:{directCompetitors:this.extractCompetitors(t,"Direct Competitors"),indirectCompetitors:this.extractCompetitors(t,"Indirect Competitors"),competitorCount:this.extractCompetitors(t,"Direct Competitors").length},marketOpportunities:{identifiedGaps:this.extractListFromSection(t,"Gap"),targetMarketInsights:this.extractListFromSection(t,"Target Market Insights"),technologyTrends:this.extractListFromSection(t,"Technology Trends")},locationAnalysis:{localMarketDynamics:this.extractSectionText(t,"Local Market Dynamics"),regionalCompetitors:this.extractListFromSection(t,"Regional Competitors"),consumerBehaviorInsights:this.extractSectionText(t,"Consumer Behavior")},nextSteps:this.extractListFromSection(t,"Next Steps"),rawMarkdown:t}}parseRefinedResearchResponse(t,r,s){return{id:`refined_research_${Date.now()}`,companyName:r.companyName,generatedAt:new Date().toISOString(),basedOnInitialResearch:s.id,detailedCompetitorAnalysis:{featureMatrix:this.extractFeatureMatrix(t),pricingAnalysis:this.extractPricingAnalysis(t),userExperienceComparison:this.extractUXComparison(t),marketPositioning:this.extractMarketPositioning(t)},deepMarketAnalysis:{validatedOpportunities:this.extractValidatedOpportunities(t),riskAssessment:this.extractRiskFactors(t),marketSizingData:this.extractMarketSizing(t),customerPersonas:this.extractCustomerPersonas(t)},strategicRecommendations:{differentiationStrategy:this.extractSectionText(t,"Differentiation Strategy"),featurePriorities:this.extractFeaturePriorities(t),marketEntryStrategy:this.extractSectionText(t,"Market Entry Strategy"),competitiveAdvantages:this.extractListFromSection(t,"Competitive Advantage")},technicalConsiderations:{requiredIntegrations:this.extractListFromSection(t,"Required Integrations"),platformConsiderations:this.extractListFromSection(t,"Platform Considerations"),scalabilityFactors:this.extractListFromSection(t,"Scalability")},rawMarkdown:t}}parseAppPlanResponse(t,r,s){return{id:`plan_${Date.now()}`,companyName:r.businessName,generatedAt:new Date().toISOString(),basedOnRefinedResearch:s||"",overview:{purpose:this.extractSectionText(t,"Purpose"),industry:r.industry,objective:this.extractSectionText(t,"Objective"),problemSolved:this.extractSectionText(t,"Problem Solved")},targetAudience:{users:this.extractSectionText(t,"Users"),needs:this.extractListFromSection(t,"Needs"),benefits:this.extractListFromSection(t,"Benefits")},features:{essential:this.extractFeatures(t,"Essential Features"),additionalAddOns:this.extractFeatures(t,"Additional Add-ons"),prioritizationNote:this.extractSectionText(t,"Feature Prioritization")},competitiveAnalysis:{competitors:this.extractSectionText(t,"Competitors"),differentiation:this.extractSectionText(t,"Differentiation")},businessBenefits:{revenueEngagement:this.extractSectionText(t,"Revenue/Engagement"),efficiency:this.extractSectionText(t,"Efficiency"),scalability:this.extractSectionText(t,"Scalability")},developmentProcess:this.extractDevelopmentPhases(t),timeline:{totalDuration:this.extractSectionText(t,"Estimated Duration"),breakdown:this.extractSectionText(t,"Total"),note:this.extractSectionText(t,"Note")},budget:{estimatedCost:this.extractSectionText(t,"Estimated Cost"),paymentTerms:this.extractSectionText(t,"Payment Terms"),flexibilityNote:this.extractSectionText(t,"Flexible Pricing")},technicalStack:{hosting:this.extractSectionText(t,"Hosting"),codeManagement:this.extractSectionText(t,"Code Management"),database:this.extractSectionText(t,"Database")},nextSteps:this.extractListFromSection(t,"Next Steps"),rawMarkdown:t}}extractSectionText(t,r){const s=new RegExp(`\\*\\*${r}\\*\\*:?\\s*([^\\n]*(?:\\n(?!\\*\\*)[^\\n]*)*)`,"i"),a=t.match(s);return a?a[1].trim():""}extractListFromSection(t,r){return this.extractSectionText(t,r).split(/[-*]/).map(a=>a.trim()).filter(a=>a.length>0)}extractCompetitors(t,r){const s=[],a=new RegExp(`### ${r}([\\s\\S]*?)(?=###|---|

## |$)`,"i"),o=t.match(a);return o&&o[1].split(`
`).filter(d=>d.trim().startsWith("-")).forEach(d=>{const y=d.match(/\*\*(.*?)\*\*/);y&&s.push({name:y[1],appFeatures:[],digitalEngagement:[],hasApp:d.toLowerCase().includes("app")})}),s}extractFeatureTable(t){return{headers:["Competitor","Online Ordering","Loyalty Program","Nutritional Info","Push Notifications","Other Features"],competitors:[]}}extractFeatures(t,r){const s=[],a=new RegExp(`${r}:([\\s\\S]*?)(?=\\*\\*|Additional Add-ons|$)`,"i"),o=t.match(a);return o&&o[1].split(`
`).filter(d=>d.trim().startsWith("-")).forEach(d=>{const y=d.match(/\*\*(.*?)\*\*:?\s*(.*)/);y&&s.push({name:y[1],description:y[2]||""})}),s}extractDevelopmentPhases(t){const r=[],s=/\d+\.\s*\*\*(.*?)\*\*\s*\((.*?)\)\s*\n\s*-\s*(.*)/g;let a;for(;(a=s.exec(t))!==null;)r.push({name:a[1],duration:a[2],description:a[3]});return r}extractFeatureMatrix(t){return{features:["Mobile App","Online Ordering","Loyalty Program","Payment Integration"],competitors:{}}}extractPricingAnalysis(t){return{averagePrice:this.extractSectionText(t,"Average Price"),pricingModels:this.extractListFromSection(t,"Pricing Models"),premiumFeatures:this.extractListFromSection(t,"Premium Features")}}extractUXComparison(t){return[]}extractMarketPositioning(t){return[]}extractValidatedOpportunities(t){return[]}extractRiskFactors(t){return[]}extractMarketSizing(t){return{totalAddressableMarket:this.extractSectionText(t,"TAM"),serviceableAddressableMarket:this.extractSectionText(t,"SAM"),serviceableObtainableMarket:this.extractSectionText(t,"SOM")}}extractCustomerPersonas(t){return[]}extractFeaturePriorities(t){return[]}storeResearchReport(t){return v(this,null,function*(){localStorage.setItem(`research_${t.id}`,JSON.stringify(t))})}storeInitialResearchReport(t){return v(this,null,function*(){localStorage.setItem(`initial_research_${t.id}`,JSON.stringify(t))})}storeRefinedResearchReport(t){return v(this,null,function*(){localStorage.setItem(`refined_research_${t.id}`,JSON.stringify(t))})}storeAppPlan(t){return v(this,null,function*(){localStorage.setItem(`plan_${t.id}`,JSON.stringify(t))})}}const F=new pe;function he(){const[h,t]=D.useState({companyName:"Ty's Juice Bar",industry:"Food & Beverage (Health & Wellness)",location:"N8 8DU, London",productsServices:"premium juices, smoothies, wellness shots",targetUsers:"Health-conscious individuals, ages 18-45"}),[r,s]=D.useState({businessName:"Ty's Juice Bar",appPurpose:"Mobile app to streamline ordering and enhance customer engagement",industry:"Food & Beverage",targetAudience:"Health-conscious individuals",budget:"$500-$2,500",timeline:"30 days"}),[a,o]=D.useState({executionTime:0,stage:"idle",currentProgress:0,currentMessage:""}),[x,d]=D.useState(!1),[y,A]=D.useState("inputs"),W=()=>v(this,null,function*(){d(!0);const n=Date.now();try{const i=yield F.executeThreeStageWorkflow(h,r,(c,M,Z)=>{o(Q=>p(m({},Q),{stage:c,currentProgress:M,currentMessage:Z}))}),l=Date.now()-n;o(c=>p(m({},c),{initialResearch:i.initialResearch,refinedResearch:i.refinedResearch,appPlan:i.appPlan,executionTime:l,stage:"complete",currentProgress:100,currentMessage:"Three-stage process completed successfully!"})),j({title:"🎉 Three-Stage Process Complete!",description:`Generated complete research workflow and app plan in ${(l/1e3).toFixed(1)}s`})}catch(i){const l=i instanceof Error?i.message:"Unknown error";o(c=>p(m({},c),{stage:"error",currentMessage:l})),j({title:"❌ Three-Stage Process Failed",description:l,variant:"destructive"})}finally{d(!1)}}),Y=()=>v(this,null,function*(){d(!0);const n=Date.now();try{o(c=>p(m({},c),{stage:"initial-research",currentProgress:50,currentMessage:"Conducting initial market research..."}));const i=yield F.executeInitialResearch(h),l=Date.now()-n;o(c=>p(m({},c),{initialResearch:i,executionTime:l,stage:"complete",currentProgress:100,currentMessage:"Initial research phase completed!"})),j({title:"🔍 Initial Research Complete!",description:`Generated initial research report in ${(l/1e3).toFixed(1)}s`})}catch(i){const l=i instanceof Error?i.message:"Unknown error";o(c=>p(m({},c),{stage:"error",currentMessage:l})),j({title:"❌ Initial Research Failed",description:l,variant:"destructive"})}finally{d(!1)}}),K=()=>v(this,null,function*(){if(!a.initialResearch){j({title:"⚠️ Missing Initial Research",description:"Please run initial research first",variant:"destructive"});return}d(!0);const n=Date.now();try{o(c=>p(m({},c),{stage:"refined-research",currentProgress:50,currentMessage:"Conducting refined research analysis..."}));const i=yield F.executeRefinedResearch(h,a.initialResearch),l=Date.now()-n;o(c=>p(m({},c),{refinedResearch:i,executionTime:l,stage:"complete",currentProgress:100,currentMessage:"Refined research phase completed!"})),j({title:"🎯 Refined Research Complete!",description:`Generated refined research report in ${(l/1e3).toFixed(1)}s`})}catch(i){const l=i instanceof Error?i.message:"Unknown error";o(c=>p(m({},c),{stage:"error",currentMessage:l})),j({title:"❌ Refined Research Failed",description:l,variant:"destructive"})}finally{d(!1)}}),J=()=>v(this,null,function*(){d(!0);const n=Date.now();try{o(c=>p(m({},c),{stage:"app-plan",currentProgress:50,currentMessage:"Generating comprehensive app plan..."}));const i=yield F.executeAppPlan(r,void 0,a.refinedResearch),l=Date.now()-n;o(c=>p(m({},c),{appPlan:i,executionTime:l,stage:"complete",currentProgress:100,currentMessage:"App plan generation completed!"})),j({title:"📱 App Plan Complete!",description:`Generated app development plan in ${(l/1e3).toFixed(1)}s`})}catch(i){const l=i instanceof Error?i.message:"Unknown error";o(c=>p(m({},c),{stage:"error",currentMessage:l})),j({title:"❌ App Plan Failed",description:l,variant:"destructive"})}finally{d(!1)}}),E=(n,i)=>{navigator.clipboard.writeText(n),j({title:"📋 Copied to Clipboard",description:`${i} copied successfully - ready for Notion!`})},$=(n,i)=>{const l=new Blob([n],{type:"text/markdown"}),c=URL.createObjectURL(l),M=document.createElement("a");M.href=c,M.download=i,M.click(),URL.revokeObjectURL(c),j({title:"💾 Downloaded",description:`${i} downloaded successfully!`})},X=n=>{switch(n){case"initial-research":return"bg-blue-500";case"refined-research":return"bg-purple-500";case"app-plan":return"bg-green-500";case"complete":return"bg-orange-500";case"error":return"bg-red-500";default:return"bg-gray-500"}};return e.jsxs("div",{className:"space-y-6",children:[e.jsx(g,{className:"bg-gradient-to-r from-gray-950 to-black border-orange-500/20",children:e.jsxs(b,{children:[e.jsxs(f,{className:"text-2xl text-white flex items-center gap-3",children:[e.jsx(w,{className:"h-6 w-6 text-orange-500"}),"Three-Stage Research & Development System"]}),e.jsx(R,{className:"text-gray-300",children:"Initial Research → Refined Research → App Plan workflow with comprehensive analysis and Notion-ready outputs"})]})}),e.jsx(g,{className:"bg-black border-orange-500/20",children:e.jsxs(u,{className:"p-6",children:[e.jsxs("div",{className:"flex items-center justify-between mb-4",children:[e.jsx("h3",{className:"text-lg font-semibold text-white",children:"Workflow Progress"}),e.jsx(T,{variant:"outline",className:"border-orange-500 text-orange-400",children:"Three-Stage System"})]}),e.jsxs("div",{className:"flex items-center gap-4",children:[e.jsxs("div",{className:`flex items-center gap-2 px-3 py-2 rounded-lg transition-all ${a.stage==="initial-research"?"bg-blue-500/20 border border-blue-500/50":a.initialResearch?"bg-green-500/20 border border-green-500/50":"bg-gray-800/50 border border-gray-600/50"}`,children:[e.jsx(w,{className:`h-4 w-4 ${a.initialResearch?"text-green-400":"text-blue-400"}`}),e.jsx("span",{className:`text-sm font-medium ${a.initialResearch?"text-green-400":"text-blue-400"}`,children:"Initial Research"})]}),e.jsx("div",{className:`h-0.5 w-8 transition-all ${a.initialResearch?"bg-green-500":"bg-gray-600"}`}),e.jsxs("div",{className:`flex items-center gap-2 px-3 py-2 rounded-lg transition-all ${a.stage==="refined-research"?"bg-purple-500/20 border border-purple-500/50":a.refinedResearch?"bg-green-500/20 border border-green-500/50":"bg-gray-800/50 border border-gray-600/50"}`,children:[e.jsx(I,{className:`h-4 w-4 ${a.refinedResearch?"text-green-400":"text-purple-400"}`}),e.jsx("span",{className:`text-sm font-medium ${a.refinedResearch?"text-green-400":"text-purple-400"}`,children:"Refined Research"})]}),e.jsx("div",{className:`h-0.5 w-8 transition-all ${a.refinedResearch?"bg-green-500":"bg-gray-600"}`}),e.jsxs("div",{className:`flex items-center gap-2 px-3 py-2 rounded-lg transition-all ${a.stage==="app-plan"||a.appPlan?"bg-green-500/20 border border-green-500/50":"bg-gray-800/50 border border-gray-600/50"}`,children:[e.jsx(C,{className:`h-4 w-4 ${a.appPlan?"text-green-400":"text-orange-400"}`}),e.jsx("span",{className:`text-sm font-medium ${a.appPlan?"text-green-400":"text-orange-400"}`,children:"App Plan"})]})]}),x&&e.jsx("div",{className:"mt-4",children:e.jsxs("div",{className:"flex items-center gap-4",children:[e.jsx(ie,{className:"h-5 w-5 animate-spin text-orange-500"}),e.jsxs("div",{className:"flex-1",children:[e.jsxs("div",{className:"flex justify-between text-sm text-gray-300 mb-2",children:[e.jsx("span",{children:a.currentMessage}),e.jsxs("span",{children:[a.currentProgress,"%"]})]}),e.jsx("div",{className:"w-full bg-gray-800 rounded-full h-2",children:e.jsx("div",{className:`h-2 rounded-full transition-all duration-300 ${X(a.stage)}`,style:{width:`${a.currentProgress}%`}})})]})]})})]})}),e.jsxs(_,{value:y,onValueChange:n=>A(n),children:[e.jsxs(q,{className:"grid w-full grid-cols-5 bg-gray-900",children:[e.jsx(k,{value:"inputs",className:"text-white data-[state=active]:bg-orange-500",children:"Input Config"}),e.jsx(k,{value:"initial",className:"text-white data-[state=active]:bg-blue-500",children:"Initial Research"}),e.jsx(k,{value:"refined",className:"text-white data-[state=active]:bg-purple-500",children:"Refined Research"}),e.jsx(k,{value:"plan",className:"text-white data-[state=active]:bg-green-500",children:"App Plan"}),e.jsx(k,{value:"structured",className:"text-white data-[state=active]:bg-gray-600",children:"Data View"})]}),e.jsxs(P,{value:"inputs",className:"space-y-6",children:[e.jsxs("div",{className:"grid grid-cols-1 lg:grid-cols-2 gap-6",children:[e.jsxs(g,{className:"bg-black border-blue-500/20",children:[e.jsxs(b,{children:[e.jsxs(f,{className:"text-blue-400 flex items-center gap-2",children:[e.jsx(w,{className:"h-5 w-5"}),"Research Input"]}),e.jsx(R,{className:"text-gray-400",children:"Configure the research parameters for both stages"})]}),e.jsxs(u,{className:"space-y-4",children:[e.jsx(S,{placeholder:"Company Name",value:h.companyName,onChange:n=>t(i=>p(m({},i),{companyName:n.target.value})),className:"bg-gray-900 border-gray-700 text-white"}),e.jsx(S,{placeholder:"Industry",value:h.industry,onChange:n=>t(i=>p(m({},i),{industry:n.target.value})),className:"bg-gray-900 border-gray-700 text-white"}),e.jsx(S,{placeholder:"Location",value:h.location,onChange:n=>t(i=>p(m({},i),{location:n.target.value})),className:"bg-gray-900 border-gray-700 text-white"}),e.jsx(B,{placeholder:"Products/Services",value:h.productsServices,onChange:n=>t(i=>p(m({},i),{productsServices:n.target.value})),className:"bg-gray-900 border-gray-700 text-white"}),e.jsx(B,{placeholder:"Target Users",value:h.targetUsers,onChange:n=>t(i=>p(m({},i),{targetUsers:n.target.value})),className:"bg-gray-900 border-gray-700 text-white"})]})]}),e.jsxs(g,{className:"bg-black border-green-500/20",children:[e.jsxs(b,{children:[e.jsxs(f,{className:"text-green-400 flex items-center gap-2",children:[e.jsx(V,{className:"h-5 w-5"}),"App Plan Input"]}),e.jsx(R,{className:"text-gray-400",children:"Configure the app development plan parameters"})]}),e.jsxs(u,{className:"space-y-4",children:[e.jsx(S,{placeholder:"Business Name",value:r.businessName,onChange:n=>s(i=>p(m({},i),{businessName:n.target.value})),className:"bg-gray-900 border-gray-700 text-white"}),e.jsx(B,{placeholder:"App Purpose",value:r.appPurpose,onChange:n=>s(i=>p(m({},i),{appPurpose:n.target.value})),className:"bg-gray-900 border-gray-700 text-white"}),e.jsx(S,{placeholder:"Industry",value:r.industry,onChange:n=>s(i=>p(m({},i),{industry:n.target.value})),className:"bg-gray-900 border-gray-700 text-white"}),e.jsx(S,{placeholder:"Target Audience",value:r.targetAudience,onChange:n=>s(i=>p(m({},i),{targetAudience:n.target.value})),className:"bg-gray-900 border-gray-700 text-white"}),e.jsx(S,{placeholder:"Budget",value:r.budget||"",onChange:n=>s(i=>p(m({},i),{budget:n.target.value})),className:"bg-gray-900 border-gray-700 text-white"}),e.jsx(S,{placeholder:"Timeline",value:r.timeline||"",onChange:n=>s(i=>p(m({},i),{timeline:n.target.value})),className:"bg-gray-900 border-gray-700 text-white"})]})]})]}),e.jsx(g,{className:"bg-black border-orange-500/20",children:e.jsxs(u,{className:"p-6",children:[e.jsxs("div",{className:"flex flex-wrap gap-4",children:[e.jsxs(N,{onClick:W,disabled:x,className:"bg-gradient-to-r from-orange-500 to-red-500 hover:from-orange-600 hover:to-red-600",children:[e.jsx(ne,{className:"h-4 w-4 mr-2"}),"Execute Full Three-Stage Workflow"]}),e.jsx(me,{orientation:"vertical",className:"h-8"}),e.jsxs(N,{onClick:Y,disabled:x,variant:"outline",className:"border-blue-500 text-blue-400 hover:bg-blue-500 hover:text-white",children:[e.jsx(w,{className:"h-4 w-4 mr-2"}),"Stage 1: Initial Research"]}),e.jsxs(N,{onClick:K,disabled:x||!a.initialResearch,variant:"outline",className:"border-purple-500 text-purple-400 hover:bg-purple-500 hover:text-white disabled:opacity-50",children:[e.jsx(I,{className:"h-4 w-4 mr-2"}),"Stage 2: Refined Research"]}),e.jsxs(N,{onClick:J,disabled:x,variant:"outline",className:"border-green-500 text-green-400 hover:bg-green-500 hover:text-white",children:[e.jsx(C,{className:"h-4 w-4 mr-2"}),"Stage 3: App Plan"]})]}),a.executionTime>0&&e.jsxs("div",{className:"mt-4 flex items-center gap-4 text-sm text-gray-400",children:[e.jsxs(T,{variant:"outline",className:"border-green-500 text-green-400",children:["⏱️ ",(a.executionTime/1e3).toFixed(1),"s"]}),e.jsx(T,{variant:"outline",className:"border-blue-500 text-blue-400",children:"🎯 Google Gemini 2.0 Flash (FREE)"}),e.jsx(T,{variant:"outline",className:"border-orange-500 text-orange-400",children:"🔄 Three-Stage System"})]})]})})]}),e.jsx(P,{value:"initial",className:"space-y-4",children:a.initialResearch?e.jsxs(g,{className:"bg-black border-blue-500/20",children:[e.jsxs(b,{children:[e.jsxs(f,{className:"text-blue-400 flex items-center justify-between",children:[e.jsxs("span",{className:"flex items-center gap-2",children:[e.jsx(w,{className:"h-5 w-5"}),"Initial Research Report for ",a.initialResearch.companyName]}),e.jsxs("div",{className:"flex gap-2",children:[e.jsxs(N,{size:"sm",variant:"outline",onClick:()=>E(a.initialResearch.rawMarkdown,"Initial Research Report"),className:"border-blue-500 text-blue-400 hover:bg-blue-500 hover:text-white",children:[e.jsx(O,{className:"h-4 w-4 mr-1"}),"Copy Markdown"]}),e.jsxs(N,{size:"sm",variant:"outline",onClick:()=>$(a.initialResearch.rawMarkdown,`${a.initialResearch.companyName.replace(/\s+/g,"_")}_initial_research.md`),className:"border-blue-500 text-blue-400 hover:bg-blue-500 hover:text-white",children:[e.jsx(L,{className:"h-4 w-4 mr-1"}),"Download"]})]})]}),e.jsx(R,{className:"text-gray-400",children:"Stage 1: Initial market research and competitor landscape analysis"})]}),e.jsx(u,{children:e.jsx("div",{className:"bg-gray-900 p-4 rounded-lg border border-gray-700",children:e.jsx("pre",{className:"text-sm text-gray-300 whitespace-pre-wrap overflow-x-auto",children:a.initialResearch.rawMarkdown})})})]}):e.jsx(g,{className:"bg-black border-gray-700",children:e.jsxs(u,{className:"p-12 text-center",children:[e.jsx(w,{className:"h-12 w-12 text-gray-600 mx-auto mb-4"}),e.jsx("p",{className:"text-gray-400",children:"No initial research generated yet. Run Stage 1 to see results."})]})})}),e.jsx(P,{value:"refined",className:"space-y-4",children:a.refinedResearch?e.jsxs(g,{className:"bg-black border-purple-500/20",children:[e.jsxs(b,{children:[e.jsxs(f,{className:"text-purple-400 flex items-center justify-between",children:[e.jsxs("span",{className:"flex items-center gap-2",children:[e.jsx(I,{className:"h-5 w-5"}),"Refined Research Report for ",a.refinedResearch.companyName]}),e.jsxs("div",{className:"flex gap-2",children:[e.jsxs(N,{size:"sm",variant:"outline",onClick:()=>E(a.refinedResearch.rawMarkdown,"Refined Research Report"),className:"border-purple-500 text-purple-400 hover:bg-purple-500 hover:text-white",children:[e.jsx(O,{className:"h-4 w-4 mr-1"}),"Copy Markdown"]}),e.jsxs(N,{size:"sm",variant:"outline",onClick:()=>$(a.refinedResearch.rawMarkdown,`${a.refinedResearch.companyName.replace(/\s+/g,"_")}_refined_research.md`),className:"border-purple-500 text-purple-400 hover:bg-purple-500 hover:text-white",children:[e.jsx(L,{className:"h-4 w-4 mr-1"}),"Download"]})]})]}),e.jsx(R,{className:"text-gray-400",children:"Stage 2: Deep analysis and strategic recommendations based on initial research"})]}),e.jsx(u,{children:e.jsx("div",{className:"bg-gray-900 p-4 rounded-lg border border-gray-700",children:e.jsx("pre",{className:"text-sm text-gray-300 whitespace-pre-wrap overflow-x-auto",children:a.refinedResearch.rawMarkdown})})})]}):e.jsx(g,{className:"bg-black border-gray-700",children:e.jsxs(u,{className:"p-12 text-center",children:[e.jsx(I,{className:"h-12 w-12 text-gray-600 mx-auto mb-4"}),e.jsx("p",{className:"text-gray-400",children:"No refined research generated yet. Run Stage 2 to see results."}),!a.initialResearch&&e.jsx("p",{className:"text-red-400 text-sm mt-2",children:"Initial research must be completed first."})]})})}),e.jsx(P,{value:"plan",className:"space-y-4",children:a.appPlan?e.jsxs(g,{className:"bg-black border-green-500/20",children:[e.jsxs(b,{children:[e.jsxs(f,{className:"text-green-400 flex items-center justify-between",children:[e.jsxs("span",{className:"flex items-center gap-2",children:[e.jsx(C,{className:"h-5 w-5"}),"App Development Plan for ",a.appPlan.companyName]}),e.jsxs("div",{className:"flex gap-2",children:[e.jsxs(N,{size:"sm",variant:"outline",onClick:()=>E(a.appPlan.rawMarkdown,"App Plan"),className:"border-green-500 text-green-400 hover:bg-green-500 hover:text-white",children:[e.jsx(O,{className:"h-4 w-4 mr-1"}),"Copy Markdown"]}),e.jsxs(N,{size:"sm",variant:"outline",onClick:()=>$(a.appPlan.rawMarkdown,`${a.appPlan.companyName.replace(/\s+/g,"_")}_app_plan.md`),className:"border-green-500 text-green-400 hover:bg-green-500 hover:text-white",children:[e.jsx(L,{className:"h-4 w-4 mr-1"}),"Download"]})]})]}),e.jsx(R,{className:"text-gray-400",children:"Stage 3: Research-backed app development plan ready for client delivery"})]}),e.jsx(u,{children:e.jsx("div",{className:"bg-gray-900 p-4 rounded-lg border border-gray-700",children:e.jsx("pre",{className:"text-sm text-gray-300 whitespace-pre-wrap overflow-x-auto",children:a.appPlan.rawMarkdown})})})]}):e.jsx(g,{className:"bg-black border-gray-700",children:e.jsxs(u,{className:"p-12 text-center",children:[e.jsx(C,{className:"h-12 w-12 text-gray-600 mx-auto mb-4"}),e.jsx("p",{className:"text-gray-400",children:"No app plan generated yet. Run Stage 3 to see results."})]})})}),e.jsx(P,{value:"structured",className:"space-y-4",children:e.jsxs("div",{className:"grid grid-cols-1 lg:grid-cols-3 gap-6",children:[a.initialResearch&&e.jsxs(g,{className:"bg-black border-blue-500/20",children:[e.jsx(b,{children:e.jsxs(f,{className:"text-blue-400 flex items-center gap-2",children:[e.jsx(w,{className:"h-5 w-5"}),"Initial Research Data"]})}),e.jsx(u,{children:e.jsxs("div",{className:"space-y-4 text-sm",children:[e.jsxs("div",{children:[e.jsx("h4",{className:"text-blue-300 font-medium mb-2",children:"Industry Overview"}),e.jsxs("div",{className:"bg-gray-900 p-3 rounded border border-gray-700",children:[e.jsxs("p",{children:[e.jsx("strong",{children:"Key Trends:"})," ",a.initialResearch.industryOverview.keyTrends.join(", ")]}),e.jsxs("p",{children:[e.jsx("strong",{children:"Growth Drivers:"})," ",a.initialResearch.industryOverview.growthDrivers.join(", ")]})]})]}),e.jsxs("div",{children:[e.jsx("h4",{className:"text-blue-300 font-medium mb-2",children:"Competitors"}),e.jsxs("div",{className:"bg-gray-900 p-3 rounded border border-gray-700",children:[e.jsxs("p",{children:[e.jsx("strong",{children:"Direct:"})," ",a.initialResearch.competitorLandscape.directCompetitors.length," found"]}),e.jsxs("p",{children:[e.jsx("strong",{children:"Indirect:"})," ",a.initialResearch.competitorLandscape.indirectCompetitors.length," found"]})]})]})]})})]}),a.refinedResearch&&e.jsxs(g,{className:"bg-black border-purple-500/20",children:[e.jsx(b,{children:e.jsxs(f,{className:"text-purple-400 flex items-center gap-2",children:[e.jsx(I,{className:"h-5 w-5"}),"Refined Research Data"]})}),e.jsx(u,{children:e.jsxs("div",{className:"space-y-4 text-sm",children:[e.jsxs("div",{children:[e.jsx("h4",{className:"text-purple-300 font-medium mb-2",children:"Strategic Analysis"}),e.jsxs("div",{className:"bg-gray-900 p-3 rounded border border-gray-700",children:[e.jsxs("p",{children:[e.jsx("strong",{children:"Opportunities:"})," ",a.refinedResearch.deepMarketAnalysis.validatedOpportunities.length," validated"]}),e.jsxs("p",{children:[e.jsx("strong",{children:"Risks:"})," ",a.refinedResearch.deepMarketAnalysis.riskAssessment.length," identified"]})]})]}),e.jsxs("div",{children:[e.jsx("h4",{className:"text-purple-300 font-medium mb-2",children:"Technical Considerations"}),e.jsxs("div",{className:"bg-gray-900 p-3 rounded border border-gray-700",children:[e.jsxs("p",{children:[e.jsx("strong",{children:"Integrations:"})," ",a.refinedResearch.technicalConsiderations.requiredIntegrations.length," required"]}),e.jsxs("p",{children:[e.jsx("strong",{children:"Platform:"})," ",a.refinedResearch.technicalConsiderations.platformConsiderations.length," considerations"]})]})]})]})})]}),a.appPlan&&e.jsxs(g,{className:"bg-black border-green-500/20",children:[e.jsx(b,{children:e.jsxs(f,{className:"text-green-400 flex items-center gap-2",children:[e.jsx(C,{className:"h-5 w-5"}),"App Plan Data"]})}),e.jsx(u,{children:e.jsxs("div",{className:"space-y-4 text-sm",children:[e.jsxs("div",{children:[e.jsx("h4",{className:"text-green-300 font-medium mb-2",children:"Features"}),e.jsxs("div",{className:"bg-gray-900 p-3 rounded border border-gray-700",children:[e.jsxs("p",{children:[e.jsx("strong",{children:"Essential:"})," ",a.appPlan.features.essential.length," features"]}),e.jsxs("p",{children:[e.jsx("strong",{children:"Add-ons:"})," ",a.appPlan.features.additionalAddOns.length," features"]})]})]}),e.jsxs("div",{children:[e.jsx("h4",{className:"text-green-300 font-medium mb-2",children:"Project Details"}),e.jsxs("div",{className:"bg-gray-900 p-3 rounded border border-gray-700",children:[e.jsxs("p",{children:[e.jsx("strong",{children:"Budget:"})," ",a.appPlan.budget.estimatedCost]}),e.jsxs("p",{children:[e.jsx("strong",{children:"Timeline:"})," ",a.appPlan.timeline.totalDuration]})]})]})]})})]})]})})]})]})}function Se(){return e.jsxs("div",{className:"container mx-auto px-4 py-8 space-y-8",children:[e.jsxs("div",{className:"text-center space-y-4",children:[e.jsxs("h1",{className:"text-4xl font-bold text-white flex items-center justify-center gap-3",children:[e.jsx(oe,{className:"h-8 w-8 text-orange-500"}),"Development & Testing Hub"]}),e.jsx("p",{className:"text-gray-400 text-lg max-w-2xl mx-auto",children:"Advanced testing tools for AI prompt systems, database integration, and app plan generation workflows"}),e.jsx(T,{variant:"outline",className:"border-orange-500 text-orange-400",children:"🚧 Development Tools - Use with caution in production"})]}),e.jsxs(_,{defaultValue:"multi-stage",className:"space-y-6",children:[e.jsxs(q,{className:"grid w-full grid-cols-3 bg-gray-900",children:[e.jsxs(k,{value:"multi-stage",className:"text-white data-[state=active]:bg-gradient-to-r data-[state=active]:from-orange-500 data-[state=active]:to-red-500",children:[e.jsx(ce,{className:"h-4 w-4 mr-2"}),"Multi-Stage Prompts"]}),e.jsxs(k,{value:"app-plan",className:"text-white data-[state=active]:bg-gradient-to-r data-[state=active]:from-blue-500 data-[state=active]:to-purple-500",children:[e.jsx(C,{className:"h-4 w-4 mr-2"}),"App Plan Testing"]}),e.jsxs(k,{value:"database",className:"text-white data-[state=active]:bg-gradient-to-r data-[state=active]:from-green-500 data-[state=active]:to-teal-500",children:[e.jsx(G,{className:"h-4 w-4 mr-2"}),"Database Tools"]})]}),e.jsxs(P,{value:"multi-stage",className:"space-y-6",children:[e.jsxs(g,{className:"bg-gradient-to-r from-gray-950 to-black border-orange-500/20",children:[e.jsxs(b,{children:[e.jsxs(f,{className:"text-white flex items-center gap-3",children:[e.jsx(w,{className:"h-6 w-6 text-orange-500"}),"Multi-Stage Prompt System",e.jsx(T,{className:"bg-orange-500 text-white",children:"NEW"})]}),e.jsx(R,{className:"text-gray-300",children:"Test the Research → App Plan workflow with structured outputs, Notion-ready formatting, and comprehensive data extraction."})]}),e.jsx(u,{children:e.jsxs("div",{className:"grid grid-cols-1 md:grid-cols-3 gap-4 mb-6",children:[e.jsxs("div",{className:"bg-blue-500/10 border border-blue-500/20 rounded-lg p-4",children:[e.jsxs("h4",{className:"text-blue-400 font-medium mb-2 flex items-center gap-2",children:[e.jsx(w,{className:"h-4 w-4"}),"Deep Research Phase"]}),e.jsx("p",{className:"text-sm text-gray-400",children:"Conducts comprehensive market research, competitor analysis, and industry insights"})]}),e.jsxs("div",{className:"bg-purple-500/10 border border-purple-500/20 rounded-lg p-4",children:[e.jsxs("h4",{className:"text-purple-400 font-medium mb-2 flex items-center gap-2",children:[e.jsx(V,{className:"h-4 w-4"}),"App Plan Generation"]}),e.jsx("p",{className:"text-sm text-gray-400",children:"Creates detailed app development plans based on research insights and client requirements"})]}),e.jsxs("div",{className:"bg-green-500/10 border border-green-500/20 rounded-lg p-4",children:[e.jsxs("h4",{className:"text-green-400 font-medium mb-2 flex items-center gap-2",children:[e.jsx(le,{className:"h-4 w-4"}),"Structured Output"]}),e.jsx("p",{className:"text-sm text-gray-400",children:"Exports Notion-ready markdown with structured data extraction for easy client presentation"})]})]})})]}),e.jsx(he,{})]}),e.jsxs(P,{value:"app-plan",className:"space-y-6",children:[e.jsxs(g,{className:"bg-gradient-to-r from-gray-950 to-black border-blue-500/20",children:[e.jsxs(b,{children:[e.jsxs(f,{className:"text-white flex items-center gap-3",children:[e.jsx(C,{className:"h-6 w-6 text-blue-500"}),"AI App Plan Testing Dashboard"]}),e.jsx(R,{className:"text-gray-300",children:"Test AI prompt strategies, validate structured parsing, and measure generation performance with real-time results."})]}),e.jsx(u,{children:e.jsxs("div",{className:"grid grid-cols-1 md:grid-cols-2 gap-4 mb-6",children:[e.jsxs("div",{className:"bg-blue-500/10 border border-blue-500/20 rounded-lg p-4",children:[e.jsx("h4",{className:"text-blue-400 font-medium mb-2",children:"Features"}),e.jsxs("ul",{className:"text-sm text-gray-400 space-y-1",children:[e.jsx("li",{children:"• Custom prompt testing"}),e.jsx("li",{children:"• Structured data parsing validation"}),e.jsx("li",{children:"• Response time measurement"}),e.jsx("li",{children:"• Google Gemini 2.0 Flash integration"})]})]}),e.jsxs("div",{className:"bg-purple-500/10 border border-purple-500/20 rounded-lg p-4",children:[e.jsx("h4",{className:"text-purple-400 font-medium mb-2",children:"Outputs"}),e.jsxs("ul",{className:"text-sm text-gray-400 space-y-1",children:[e.jsx("li",{children:"• Raw AI response text"}),e.jsx("li",{children:"• Parsed structured data"}),e.jsx("li",{children:"• Parsing success metrics"}),e.jsx("li",{children:"• Cost analysis (FREE with Gemini)"})]})]})]})})]}),e.jsx(de,{})]}),e.jsx(P,{value:"database",className:"space-y-6",children:e.jsxs(g,{className:"bg-gradient-to-r from-gray-950 to-black border-green-500/20",children:[e.jsxs(b,{children:[e.jsxs(f,{className:"text-white flex items-center gap-3",children:[e.jsx(G,{className:"h-6 w-6 text-green-500"}),"Database & Integration Tools"]}),e.jsx(R,{className:"text-gray-300",children:"Monitor Supabase connections, test edge functions, and validate data persistence workflows."})]}),e.jsx(u,{children:e.jsxs("div",{className:"space-y-4",children:[e.jsxs("div",{className:"bg-green-500/10 border border-green-500/20 rounded-lg p-4",children:[e.jsx("h4",{className:"text-green-400 font-medium mb-2",children:"🚧 Coming Soon"}),e.jsx("p",{className:"text-sm text-gray-400",children:"Database testing tools, connection monitoring, and data validation utilities will be available in the next development cycle."})]}),e.jsxs("div",{className:"grid grid-cols-1 md:grid-cols-2 gap-4",children:[e.jsxs(g,{className:"bg-black border-gray-700",children:[e.jsx(b,{children:e.jsx(f,{className:"text-gray-400 text-sm",children:"Planned Features"})}),e.jsx(u,{className:"text-sm text-gray-500",children:e.jsxs("ul",{className:"space-y-1",children:[e.jsx("li",{children:"• Supabase connection testing"}),e.jsx("li",{children:"• Edge function monitoring"}),e.jsx("li",{children:"• Data migration validation"}),e.jsx("li",{children:"• Real-time subscription testing"})]})})]}),e.jsxs(g,{className:"bg-black border-gray-700",children:[e.jsx(b,{children:e.jsx(f,{className:"text-gray-400 text-sm",children:"Integration Status"})}),e.jsx(u,{className:"text-sm text-gray-500",children:e.jsxs("ul",{className:"space-y-1",children:[e.jsx("li",{children:"✅ Google Gemini API"}),e.jsx("li",{children:"✅ Supabase Client"}),e.jsx("li",{children:"🔄 Edge Functions"}),e.jsx("li",{children:"⏳ Database Schemas"})]})})]})]})]})})]})})]})]})}export{Se as default};
