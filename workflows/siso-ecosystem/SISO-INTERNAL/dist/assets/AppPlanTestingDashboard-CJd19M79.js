var W=Object.defineProperty,Y=Object.defineProperties;var z=Object.getOwnPropertyDescriptors;var k=Object.getOwnPropertySymbols;var K=Object.prototype.hasOwnProperty,J=Object.prototype.propertyIsEnumerable;var F=(r,t,n)=>t in r?W(r,t,{enumerable:!0,configurable:!0,writable:!0,value:n}):r[t]=n,o=(r,t)=>{for(var n in t||(t={}))K.call(t,n)&&F(r,n,t[n]);if(k)for(var n of k(t))J.call(t,n)&&F(r,n,t[n]);return r},d=(r,t)=>Y(r,z(t));var X=(r,t,n)=>new Promise((j,g)=>{var x=i=>{try{p(n.next(i))}catch(u){g(u)}},v=i=>{try{p(n.throw(i))}catch(u){g(u)}},p=i=>i.done?j(i.value):Promise.resolve(i.value).then(x,v);p((n=n.apply(r,t)).next())});import{r as h,j as e,bn as $,O as Q,b5 as q,bq as Z,cD as ee,b0 as se}from"./vendor-C50ijZWh.js";import{B as D,C as w,a as E,b as f,c as S,N as m,d as R,I as y,s as ae}from"./index-Blbobipf.js";import{T as U}from"./textarea-B56zo4Tx.js";import{T as M,a as O,b,c as N}from"./tabs-CsM4ZGNr.js";import{S as C}from"./scroll-area-D4x0YgaW.js";import{S as te}from"./separator-BNrJR0ZO.js";import{A as re,a as ne}from"./alert-y6vZCamD.js";import"./libs-B3eAAgHd.js";import"./supabase-D8k0GRjn.js";const ye=()=>{const[r,t]=h.useState({businessName:"TechStart Solutions",appPurpose:"Customer relationship management for small businesses",industry:"Software & Technology",targetAudience:"Small business owners with 10-50 employees",budget:"£20,000 - £40,000",timeline:"12-16 weeks"}),[n,j]=h.useState(""),[g,x]=h.useState(!1),[v,p]=h.useState([]),[i,u]=h.useState(!1),[l,A]=h.useState(null),L=[{name:"E-commerce Startup",data:{businessName:"Fashion Forward",appPurpose:"Online fashion marketplace for sustainable clothing",industry:"E-commerce & Retail",targetAudience:"Eco-conscious millennials aged 25-40",budget:"£50,000 - £80,000",timeline:"16-20 weeks"}},{name:"HealthTech App",data:{businessName:"WellnessTrack",appPurpose:"Mental health and wellness tracking platform",industry:"Healthcare & Wellness",targetAudience:"Adults seeking mental health support (18-65)",budget:"£30,000 - £60,000",timeline:"20-24 weeks"}},{name:"FinTech Solution",data:{businessName:"SmartBudget",appPurpose:"Personal finance management and investment tracking",industry:"Financial Services",targetAudience:"Young professionals starting their investment journey",budget:"£40,000 - £70,000",timeline:"18-22 weeks"}}],P=[{name:"Structured Business Plan",prompt:`Create a comprehensive app development plan with the following EXACT structure:

## EXECUTIVE SUMMARY
[2-3 paragraph overview]

## CORE FEATURES (Rank by Priority)
### High Priority Features:
- Feature 1: [Name] - [Description] - [User Story]
- Feature 2: [Name] - [Description] - [User Story]

### Medium Priority Features:
- Feature 3: [Name] - [Description] - [User Story]
- Feature 4: [Name] - [Description] - [User Story]

## TECHNICAL ARCHITECTURE
**Platform Recommendation:** [Native/Cross-platform/Web]
**Tech Stack:**
- Frontend: [Technology]
- Backend: [Technology]
- Database: [Technology]
- APIs: [List key integrations]

## DEVELOPMENT PHASES
### Phase 1: MVP (Weeks 1-8)
- Deliverables: [List]
- Features: [List]

### Phase 2: Enhancement (Weeks 9-16)
- Deliverables: [List]
- Features: [List]

## COST BREAKDOWN (GBP)
- Development: £[amount]
- Design: £[amount]
- Testing: £[amount]
- Total: £[amount]

## TIMELINE: [X] weeks total

Format this as a professional business document.`},{name:"JSON-Friendly Format",prompt:`Respond with a structured app development plan that includes clear sections that can be easily parsed:

START_EXECUTIVE_SUMMARY
[Executive summary content]
END_EXECUTIVE_SUMMARY

START_FEATURES
HIGH_PRIORITY:
- User Authentication and Profile Management
- Core Business Functionality
- Basic Reporting Dashboard

MEDIUM_PRIORITY:
- Advanced Analytics
- Third-party Integrations
- Enhanced User Experience

LOW_PRIORITY:
- AI-powered Features
- Advanced Customization
- Additional Modules
END_FEATURES

START_TECH_STACK
Platform: [recommendation]
Frontend: [technology]
Backend: [technology]
Database: [technology]
END_TECH_STACK

START_COSTS
Development: £[amount]
Design: £[amount]
Testing: £[amount]
Total: £[amount]
END_COSTS

START_TIMELINE
Total Duration: [X weeks]
Phase 1: [weeks] - [deliverables]
Phase 2: [weeks] - [deliverables]
END_TIMELINE

Use this exact format for easy parsing.`},{name:"Markdown Structured",prompt:`Create an app development plan using this EXACT markdown structure:

# APP DEVELOPMENT PLAN: {businessName}

## 📋 EXECUTIVE SUMMARY
{2-3 paragraph executive summary}

## 🚀 CORE FEATURES
### Priority: HIGH
1. **Feature Name** - Description (User Story: As a [user], I want [goal] so that [benefit])
2. **Feature Name** - Description (User Story: As a [user], I want [goal] so that [benefit])

### Priority: MEDIUM
3. **Feature Name** - Description (User Story: As a [user], I want [goal] so that [benefit])
4. **Feature Name** - Description (User Story: As a [user], I want [goal] so that [benefit])

## 🔧 TECHNICAL APPROACH
- **Platform**: [Native iOS/Android | Cross-platform | Progressive Web App]
- **Frontend**: [React Native | Flutter | React]
- **Backend**: [Node.js | Python | .NET]
- **Database**: [PostgreSQL | MongoDB | Firebase]

## 💰 INVESTMENT BREAKDOWN
| Category | Cost (GBP) |
|----------|------------|
| Development | £XX,XXX |
| Design | £X,XXX |
| Testing | £X,XXX |
| **Total** | **£XX,XXX** |

## ⏱️ DELIVERY TIMELINE
**Total Duration**: XX weeks

**Phase 1 (Weeks 1-X)**: MVP Development
- Core features implementation
- Basic UI/UX design
- Initial testing

**Phase 2 (Weeks X-XX)**: Enhancement & Launch
- Advanced features
- Performance optimization
- Production deployment

Use this EXACT format including emojis and markdown structure.`}],B=()=>X(void 0,null,function*(){u(!0);const s=Date.now();try{const a=g&&n.trim()?n:P[0].prompt,{data:c,error:T}=yield ae.functions.invoke("generate-app-plan",{body:{businessData:r,options:{customPrompt:g?n:void 0,testMode:!0}}});if(T)throw new Error(T.message||"Failed to generate app plan");const H=Date.now()-s,I={id:Date.now().toString(),timestamp:new Date().toISOString(),businessData:o({},r),prompt:a,rawResponse:c.rawResponse||"No response received",structuredPlan:c.generatedPlan||{},parseSuccess:c.success||!1,responseTime:H,costSavings:c.costSavings||"FREE - Google Gemini"};p(V=>[I,...V]),A(I)}catch(a){console.error("Testing error:",a);const c={id:Date.now().toString(),timestamp:new Date().toISOString(),businessData:o({},r),prompt:g?n:P[0].prompt,rawResponse:`Error: ${a instanceof Error?a.message:String(a)}

⚠️  Troubleshooting Tips:
- Check if the Supabase project is connected properly
- Verify the Google API key is set in Supabase secrets
- Ensure the edge function is deployed

🔧 Technical Details:
${a instanceof Error?a.stack||"No stack trace available":"Unknown error type"}`,structuredPlan:{error:"Failed to generate plan due to API error"},parseSuccess:!1,responseTime:Date.now()-s,costSavings:"FREE - Google Gemini"};p(T=>[c,...T]),A(c)}finally{u(!1)}}),G=s=>{t(s.data)},_=s=>{navigator.clipboard.writeText(s)};return e.jsx("div",{className:"min-h-screen bg-gray-900 text-white p-6",children:e.jsxs("div",{className:"max-w-7xl mx-auto",children:[e.jsxs("div",{className:"mb-8",children:[e.jsx("h1",{className:"text-3xl font-bold text-white mb-2",children:"🧪 AI App Plan Testing Dashboard"}),e.jsx("p",{className:"text-gray-300",children:"Test different prompts and client scenarios with Google Gemini to optimize app plan generation"}),e.jsxs("div",{className:"flex gap-2 mt-4",children:[e.jsxs(D,{variant:"secondary",className:"bg-green-900 text-green-100",children:[e.jsx($,{className:"w-3 h-3 mr-1"}),"Google Gemini 2.0 Flash (FREE)"]}),e.jsx(D,{variant:"secondary",className:"bg-blue-900 text-blue-100",children:"100% Cost Savings vs OpenAI"})]})]}),e.jsxs("div",{className:"grid grid-cols-1 lg:grid-cols-2 gap-6",children:[e.jsxs("div",{className:"space-y-6",children:[e.jsxs(w,{className:"bg-gray-800 border-gray-700",children:[e.jsx(E,{children:e.jsxs(f,{className:"text-white flex items-center gap-2",children:[e.jsx(Q,{className:"w-5 h-5"}),"Client Business Data"]})}),e.jsxs(S,{className:"space-y-4",children:[e.jsxs("div",{children:[e.jsx(m,{className:"text-gray-300 mb-2 block",children:"Quick Test Scenarios"}),e.jsx("div",{className:"flex flex-wrap gap-2",children:L.map((s,a)=>e.jsx(R,{variant:"outline",size:"sm",onClick:()=>G(s),className:"bg-gray-700 border-gray-600 text-gray-200 hover:bg-gray-600",children:s.name},a))})]}),e.jsx(te,{className:"bg-gray-700"}),e.jsxs("div",{className:"grid grid-cols-1 gap-4",children:[e.jsxs("div",{children:[e.jsx(m,{className:"text-gray-300",children:"Business Name"}),e.jsx(y,{value:r.businessName,onChange:s=>t(a=>d(o({},a),{businessName:s.target.value})),className:"bg-gray-700 border-gray-600 text-white"})]}),e.jsxs("div",{children:[e.jsx(m,{className:"text-gray-300",children:"App Purpose"}),e.jsx(U,{value:r.appPurpose,onChange:s=>t(a=>d(o({},a),{appPurpose:s.target.value})),className:"bg-gray-700 border-gray-600 text-white",rows:2})]}),e.jsxs("div",{className:"grid grid-cols-2 gap-4",children:[e.jsxs("div",{children:[e.jsx(m,{className:"text-gray-300",children:"Industry"}),e.jsx(y,{value:r.industry,onChange:s=>t(a=>d(o({},a),{industry:s.target.value})),className:"bg-gray-700 border-gray-600 text-white"})]}),e.jsxs("div",{children:[e.jsx(m,{className:"text-gray-300",children:"Target Audience"}),e.jsx(y,{value:r.targetAudience,onChange:s=>t(a=>d(o({},a),{targetAudience:s.target.value})),className:"bg-gray-700 border-gray-600 text-white"})]})]}),e.jsxs("div",{className:"grid grid-cols-2 gap-4",children:[e.jsxs("div",{children:[e.jsx(m,{className:"text-gray-300",children:"Budget"}),e.jsx(y,{value:r.budget,onChange:s=>t(a=>d(o({},a),{budget:s.target.value})),className:"bg-gray-700 border-gray-600 text-white"})]}),e.jsxs("div",{children:[e.jsx(m,{className:"text-gray-300",children:"Timeline"}),e.jsx(y,{value:r.timeline,onChange:s=>t(a=>d(o({},a),{timeline:s.target.value})),className:"bg-gray-700 border-gray-600 text-white"})]})]})]})]})]}),e.jsxs(w,{className:"bg-gray-800 border-gray-700",children:[e.jsx(E,{children:e.jsx(f,{className:"text-white",children:"Prompt Engineering"})}),e.jsx(S,{className:"space-y-4",children:e.jsxs(M,{defaultValue:"templates",className:"w-full",children:[e.jsxs(O,{className:"grid w-full grid-cols-2 bg-gray-700",children:[e.jsx(b,{value:"templates",className:"data-[state=active]:bg-gray-600 text-gray-200",onClick:()=>x(!1),children:"Templates"}),e.jsx(b,{value:"custom",className:"data-[state=active]:bg-gray-600 text-gray-200",onClick:()=>x(!0),children:"Custom"})]}),e.jsx(N,{value:"templates",className:"space-y-3",children:P.map((s,a)=>e.jsxs("div",{className:"p-3 bg-gray-700 rounded-lg border border-gray-600 cursor-pointer hover:bg-gray-600",onClick:()=>{j(s.prompt),x(!1)},children:[e.jsx("h4",{className:"font-medium text-white mb-1",children:s.name}),e.jsxs("p",{className:"text-sm text-gray-300 line-clamp-2",children:[s.prompt.substring(0,100),"..."]})]},a))}),e.jsx(N,{value:"custom",children:e.jsx(U,{value:n,onChange:s=>j(s.target.value),placeholder:"Enter your custom prompt here...",className:"bg-gray-700 border-gray-600 text-white min-h-[200px]"})})]})})]}),e.jsx(R,{onClick:B,disabled:i,className:"w-full bg-blue-600 hover:bg-blue-700 text-white py-3",size:"lg",children:i?e.jsxs(e.Fragment,{children:[e.jsx(q,{className:"w-4 h-4 mr-2 animate-spin"}),"Generating with Gemini..."]}):e.jsxs(e.Fragment,{children:[e.jsx(Z,{className:"w-4 h-4 mr-2"}),"Generate App Plan (FREE)"]})})]}),e.jsxs("div",{className:"space-y-6",children:[e.jsxs(w,{className:"bg-gray-800 border-gray-700",children:[e.jsx(E,{children:e.jsx(f,{className:"text-white",children:"Test Results History"})}),e.jsx(S,{children:e.jsx(C,{className:"h-[300px]",children:v.length===0?e.jsx("div",{className:"text-center text-gray-400 py-8",children:"No test results yet. Generate your first app plan!"}):e.jsx("div",{className:"space-y-3",children:v.map(s=>e.jsxs("div",{className:`p-3 rounded-lg border cursor-pointer ${(l==null?void 0:l.id)===s.id?"bg-blue-900 border-blue-600":"bg-gray-700 border-gray-600 hover:bg-gray-600"}`,onClick:()=>A(s),children:[e.jsxs("div",{className:"flex justify-between items-start mb-2",children:[e.jsx("h4",{className:"font-medium text-white text-sm",children:s.businessData.businessName}),e.jsx("div",{className:"flex gap-1",children:e.jsx(D,{variant:s.parseSuccess?"default":"destructive",className:"text-xs",children:s.parseSuccess?"Success":"Failed"})})]}),e.jsx("p",{className:"text-xs text-gray-300 mb-1",children:s.businessData.industry}),e.jsxs("div",{className:"flex justify-between text-xs text-gray-400",children:[e.jsx("span",{children:new Date(s.timestamp).toLocaleTimeString()}),e.jsxs("span",{children:[s.responseTime,"ms"]})]})]},s.id))})})})]}),l&&e.jsxs(w,{className:"bg-gray-800 border-gray-700",children:[e.jsx(E,{children:e.jsxs(f,{className:"text-white flex items-center justify-between",children:["Result Analysis",e.jsx("div",{className:"flex gap-2",children:e.jsxs(R,{size:"sm",variant:"outline",onClick:()=>_(l.rawResponse),className:"bg-gray-700 border-gray-600 text-gray-200",children:[e.jsx(ee,{className:"w-3 h-3 mr-1"}),"Copy Raw"]})})]})}),e.jsxs(S,{children:[e.jsxs(M,{defaultValue:"structured",className:"w-full",children:[e.jsxs(O,{className:"grid w-full grid-cols-3 bg-gray-700",children:[e.jsx(b,{value:"structured",className:"data-[state=active]:bg-gray-600 text-gray-200",children:"Structured"}),e.jsx(b,{value:"raw",className:"data-[state=active]:bg-gray-600 text-gray-200",children:"Raw Response"}),e.jsx(b,{value:"prompt",className:"data-[state=active]:bg-gray-600 text-gray-200",children:"Prompt Used"})]}),e.jsx(N,{value:"structured",className:"mt-4",children:e.jsx(C,{className:"h-[400px]",children:e.jsx("div",{className:"bg-gray-900 p-4 rounded-lg",children:e.jsx("pre",{className:"text-sm text-gray-300 whitespace-pre-wrap",children:JSON.stringify(l.structuredPlan,null,2)})})})}),e.jsx(N,{value:"raw",className:"mt-4",children:e.jsx(C,{className:"h-[400px]",children:e.jsx("div",{className:"bg-gray-900 p-4 rounded-lg",children:e.jsx("div",{className:"text-sm text-gray-300 whitespace-pre-wrap",children:l.rawResponse})})})}),e.jsx(N,{value:"prompt",className:"mt-4",children:e.jsx(C,{className:"h-[400px]",children:e.jsx("div",{className:"bg-gray-900 p-4 rounded-lg",children:e.jsx("div",{className:"text-sm text-gray-300 whitespace-pre-wrap",children:l.prompt})})})})]}),e.jsxs("div",{className:"mt-4 grid grid-cols-2 gap-4",children:[e.jsxs("div",{className:"bg-gray-900 p-3 rounded-lg",children:[e.jsx("div",{className:"text-xs text-gray-400",children:"Response Time"}),e.jsxs("div",{className:"text-lg font-bold text-white",children:[l.responseTime,"ms"]})]}),e.jsxs("div",{className:"bg-gray-900 p-3 rounded-lg",children:[e.jsx("div",{className:"text-xs text-gray-400",children:"Cost"}),e.jsx("div",{className:"text-lg font-bold text-green-400",children:"FREE"})]})]})]})]})]})]}),e.jsxs(re,{className:"mt-8 bg-blue-900 border-blue-700",children:[e.jsx(se,{className:"h-4 w-4"}),e.jsxs(ne,{className:"text-blue-100",children:[e.jsx("strong",{children:"💡 Testing Tips:"}),' Try different prompt templates to see how Gemini structures responses. Use the "JSON-Friendly" template for easier parsing, or "Markdown Structured" for beautiful formatting. The structured data shows how well the parsing worked!']})]})]})})};export{ye as default};
