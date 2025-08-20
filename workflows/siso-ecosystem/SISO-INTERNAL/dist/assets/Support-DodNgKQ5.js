var Ne=Object.defineProperty,Se=Object.defineProperties;var ke=Object.getOwnPropertyDescriptors;var ce=Object.getOwnPropertySymbols;var Ce=Object.prototype.hasOwnProperty,Pe=Object.prototype.propertyIsEnumerable;var de=(l,c,n)=>c in l?Ne(l,c,{enumerable:!0,configurable:!0,writable:!0,value:n}):l[c]=n,C=(l,c)=>{for(var n in c||(c={}))Ce.call(c,n)&&de(l,n,c[n]);if(ce)for(var n of ce(c))Pe.call(c,n)&&de(l,n,c[n]);return l},P=(l,c)=>Se(l,ke(c));var te=(l,c,n)=>new Promise((r,o)=>{var m=f=>{try{N(n.next(f))}catch(v){o(v)}},b=f=>{try{N(n.throw(f))}catch(v){o(v)}},N=f=>f.done?r(f.value):Promise.resolve(f.value).then(m,b);N((n=n.apply(l,c)).next())});import{r as u,j as e,m as g,bT as $,bl as ee,N as _,c0 as se,ag as Te,ca as ie,fH as Ae,fI as Me,X as Y,aY as ne,cD as Re,fJ as pe,fK as Ie,b5 as me,bw as ue,aa as De,dw as Be,ah as J,cE as qe,f as X,H as ae,bn as he,aX as Fe,b3 as Ue,a_ as ge,bx as Ee,bG as ze,cA as Le,bp as Oe,bU as He,a2 as Ge,M as We,br as Ve,U as Qe,c9 as Ke,a$ as $e,b7 as Ye,bS as _e,K as Je,fL as Xe}from"./vendor-C50ijZWh.js";import{P as Ze,D as es}from"./dashboard-greeting-card-DLEpxwt_.js";import{I as Q,d as h,C as F,a as oe,B as R,b as le,g as ss,c as H,h as A,N as T,K as Z}from"./index-Blbobipf.js";import{T as ts,a as as,b as is,c as rs}from"./tabs-CsM4ZGNr.js";import"./table-DWISvnW8.js";import{S as xe,a as fe,b as ye,c as be,d as O}from"./select-Ba1tjTaP.js";import{S as ns}from"./scroll-area-D4x0YgaW.js";import{T as re}from"./textarea-B56zo4Tx.js";import{R as os,a as ls}from"./radio-group-BsuxOhY4.js";import"./libs-B3eAAgHd.js";import"./supabase-D8k0GRjn.js";function cs({title:l="Resources & Support",subtitle:c="Find help, documentation, and manage your profile all in one place",searchPlaceholder:n="Search for help articles...",featuredArticles:r=[],quickHelpCards:o=[],helpCenterCards:m=[],helpCategories:b=[],backgroundImage:N="/images/resources-bg.jpg",className:f="",onSearch:v,defaultTab:S="getting-started"}){const[p,j]=u.useState(S),[U,D]=u.useState(""),E={hidden:{opacity:0,y:20},visible:{opacity:1,y:0,transition:{duration:.6}}},z=(i="orange")=>{const t={orange:"text-orange-400",blue:"text-blue-400",purple:"text-purple-400",green:"text-green-400"};return t[i]||t.orange},B=(i="orange")=>{const t={orange:{bg:"bg-orange-500/20 border-orange-500/30",icon:"text-orange-400",button:"bg-orange-600 hover:bg-orange-700"},purple:{bg:"bg-purple-500/20 border-purple-500/30",icon:"text-purple-400",button:"border-purple-500/30 text-purple-300 hover:bg-purple-500/10 hover:text-purple-200"},blue:{bg:"bg-blue-500/20 border-blue-500/30",icon:"text-blue-400",button:"border-blue-500/30 text-blue-300 hover:bg-blue-500/10 hover:text-blue-200"},green:{bg:"bg-green-500/20 border-green-500/30",icon:"text-green-400",button:"border-green-500/30 text-green-300 hover:bg-green-500/10 hover:text-green-200"}};return t[i]||t.orange},I=i=>{D(i),v==null||v(i)};return e.jsxs("div",{className:`space-y-12 ${f}`,children:[e.jsxs(g.div,{initial:"hidden",animate:"visible",variants:E,className:"relative mb-10 rounded-xl overflow-hidden",children:[e.jsx("div",{className:"absolute inset-0 bg-gradient-to-r from-black/80 to-black/40 z-10"}),e.jsx("div",{className:"absolute inset-0 bg-cover bg-center z-0 opacity-40",style:{backgroundImage:`url('${N}')`}}),e.jsxs("div",{className:"relative z-20 px-8 py-12 md:py-16 max-w-3xl",children:[e.jsx("h1",{className:"text-4xl md:text-5xl font-bold mb-4 text-white",children:l}),e.jsx("p",{className:"text-xl text-gray-200 mb-6",children:c}),e.jsxs("div",{className:"relative max-w-md",children:[e.jsx(Q,{type:"text",placeholder:n,className:"pr-10 bg-black/50 border-gray-700 backdrop-blur-sm focus:ring-orange-500/50 text-white",value:U,onChange:i=>I(i.target.value)}),e.jsx($,{className:"absolute right-3 top-2.5 h-5 w-5 text-gray-300"})]})]})]}),r.length>0&&e.jsxs(g.div,{initial:{opacity:0,y:20},animate:{opacity:1,y:0},transition:{duration:.5,delay:.2},className:"mb-12",children:[e.jsxs("div",{className:"flex items-center justify-between mb-6",children:[e.jsxs("div",{className:"flex items-center gap-2",children:[e.jsx(ee,{className:"h-5 w-5 text-orange-400"}),e.jsx("h2",{className:"text-2xl font-bold text-white",children:"Featured Resources"})]}),e.jsxs(h,{variant:"link",className:"text-orange-400 hover:text-white",children:["View all ",e.jsx(_,{className:"ml-1 h-4 w-4"})]})]}),e.jsx("div",{className:"grid grid-cols-1 md:grid-cols-3 gap-6",children:r.map((i,t)=>e.jsx(g.div,{whileHover:{scale:1.02,transition:{duration:.2}},className:"cursor-pointer",onClick:()=>j(i.category),children:e.jsx(F,{className:"bg-black/60 border-gray-800 h-full hover:border-orange-400/40 hover:bg-black/70 transition-all shadow-lg shadow-black/20",children:e.jsxs(oe,{className:"pb-2",children:[e.jsxs("div",{className:"flex justify-between items-start",children:[e.jsx("div",{className:"h-10 w-10 rounded-full bg-black/80 border border-gray-700 flex items-center justify-center",children:e.jsx(i.icon,{className:`h-5 w-5 ${z(i.color)}`})}),e.jsx(R,{variant:"secondary",className:"bg-black/70 text-gray-300 border-gray-700",children:i.tag})]}),e.jsx(le,{className:"mt-4 text-xl text-white",children:i.title}),e.jsx(ss,{className:"text-gray-300",children:i.description})]})})},t))})]}),o.length>0&&e.jsxs(g.div,{initial:{opacity:0,y:20},animate:{opacity:1,y:0},transition:{duration:.5,delay:.3},className:"mb-12",children:[e.jsxs("div",{className:"flex items-center gap-2 mb-6",children:[e.jsx(se,{className:"h-5 w-5 text-orange-400"}),e.jsx("h2",{className:"text-2xl font-bold text-white",children:"Need Help?"})]}),e.jsx("div",{className:"grid grid-cols-1 md:grid-cols-2 gap-6",children:o.map((i,t)=>e.jsx(F,{className:"bg-gradient-to-br from-black/70 to-black/50 border-gray-800 hover:border-orange-400/40 transition-all shadow-lg",children:e.jsx(H,{className:"pt-6",children:e.jsxs("div",{className:"flex gap-4 items-start",children:[e.jsx("div",{className:`h-12 w-12 rounded-full ${i.variant==="primary"?"bg-orange-500/20 border-orange-500/30":"bg-purple-500/20 border-purple-500/30"} border flex items-center justify-center flex-shrink-0`,children:e.jsx(i.icon,{className:`h-6 w-6 ${i.variant==="primary"?"text-orange-400":"text-purple-400"}`})}),e.jsxs("div",{children:[e.jsx("h3",{className:"text-xl font-semibold mb-2 text-white",children:i.title}),e.jsx("p",{className:"text-gray-300 mb-4",children:i.description}),e.jsx(h,{onClick:i.onAction,className:i.variant==="primary"?"bg-orange-600 hover:bg-orange-700 text-white shadow-md":"border-purple-500/30 text-purple-300 hover:bg-purple-500/10 hover:text-purple-200 shadow-md",variant:i.variant==="primary"?"default":"outline",children:i.buttonText})]})]})})},t))})]}),b.length>0&&e.jsx(g.div,{initial:{opacity:0,y:20},animate:{opacity:1,y:0},transition:{duration:.5,delay:.4},children:e.jsx(F,{className:"bg-black/60 border-gray-800 backdrop-blur-sm p-6 shadow-xl",children:e.jsxs(ts,{defaultValue:S,value:p,onValueChange:j,className:"w-full",children:[e.jsx(as,{className:"grid w-full bg-black/70 p-1",style:{gridTemplateColumns:`repeat(${b.length}, 1fr)`},children:b.map(i=>e.jsxs(is,{value:i.id,className:"flex items-center gap-2 data-[state=active]:bg-orange-500/30 data-[state=active]:text-white text-gray-300",children:[e.jsx(i.icon,{className:"h-4 w-4"}),e.jsx("span",{children:i.label})]},i.id))}),b.map(i=>e.jsx(rs,{value:i.id,className:"mt-6 focus-visible:outline-none",children:i.content},i.id))]})})}),m.length>0&&e.jsxs(g.div,{initial:{opacity:0,y:20},animate:{opacity:1,y:0},transition:{duration:.5,delay:.5},className:"mt-12 mb-8",children:[e.jsxs("div",{className:"flex items-center gap-2 mb-6",children:[e.jsx(Te,{className:"h-5 w-5 text-orange-400"}),e.jsx("h2",{className:"text-2xl font-bold text-white",children:"Help Center"})]}),e.jsx("div",{className:"grid grid-cols-1 md:grid-cols-3 gap-6",children:m.map((i,t)=>{const a=B(i.color);return e.jsx(F,{className:"bg-black/70 border-gray-800 hover:border-orange-400/40 transition-all shadow-lg",children:e.jsxs(H,{className:"pt-6 flex flex-col items-center text-center",children:[e.jsx("div",{className:`h-16 w-16 rounded-full ${a.bg} border flex items-center justify-center mb-4`,children:e.jsx(i.icon,{className:`h-8 w-8 ${a.icon}`})}),e.jsx("h3",{className:"text-xl font-semibold mb-2 text-white",children:i.title}),e.jsx("p",{className:"text-gray-300 mb-4",children:i.description}),e.jsx(h,{onClick:i.onAction,className:i.color==="orange"?a.button:`${a.button} shadow-md`,variant:i.color==="orange"?"default":"outline",children:i.buttonText})]})},t)})})]})]})}function ds({isOpen:l,onToggle:c,className:n}){const[r,o]=u.useState([{id:"1",type:"ai",content:`👋 Hi! I'm your SISO Partnership Assistant. I can help you with:

• Partnership program questions
• Commission and payment inquiries
• Referral process guidance
• Technical support
• Best practices for success

What would you like to know?`,timestamp:new Date,sources:[]}]),[m,b]=u.useState(""),[N,f]=u.useState(!1),[v,S]=u.useState(!1),p=u.useRef(null),j=u.useRef(null),U=()=>{var a;(a=p.current)==null||a.scrollIntoView({behavior:"smooth"})};u.useEffect(()=>{U()},[r]);const D={commission:{keywords:["commission","payment","earnings","rate","percentage","money"],content:`SISO Partnership Commission Structure:

• **Standard Rate**: 15% for basic services
• **Premium Rate**: 20% for enterprise clients
• **Recurring**: 10% monthly for ongoing services
• **Bonus Tiers**: Up to 25% for top performers

**Payment Schedule**: Monthly payouts for earnings above £100
**Payment Methods**: Bank transfer, PayPal, Wise`},referrals:{keywords:["referral","client","submit","refer","new client","lead"],content:`How to Submit Referrals:

1. **Complete your partner profile** first
2. **Use your unique referral link** from the dashboard
3. **Gather client information**: Company details, project scope, budget
4. **Submit through the referral form** in your dashboard
5. **Follow up** within 48 hours

**Best Practices**:
• Warm introductions work best
• Understand client needs thoroughly
• Provide clear value propositions`},tracking:{keywords:["track","tracking","status","progress","dashboard"],content:`Referral Tracking System:

• **Real-time updates** on referral status
• **Commission calculator** shows potential earnings
• **Progress notifications** via email and dashboard
• **Performance analytics** to optimize results

**Statuses**:
• Submitted → Under Review → Approved → In Progress → Completed`},requirements:{keywords:["requirements","qualify","criteria","eligibility","join"],content:`Partnership Requirements:

• **Professional network** in business/tech
• **Commitment** to quality referrals
• **Understanding** of SISO services
• **Active communication** with potential clients

**No upfront costs** or minimum commitments required!`},support:{keywords:["help","support","contact","problem","issue","assistance"],content:`Support Channels:

• **Live Chat**: Available 9AM-6PM GMT (< 5 min response)
• **Email**: partners@siso.agency (< 4 hours)
• **Phone**: +44 (0) 20 1234 5678
• **Training Hub**: Self-paced learning resources

**Emergency Support**: For urgent issues, mark emails as 'URGENT'`},training:{keywords:["training","learn","course","education","guide","tutorial"],content:`Partnership Training Resources:

• **Video Library**: 45+ training videos
• **Partner Handbook**: Comprehensive PDF guide
• **Live Workshops**: Monthly Q&A sessions
• **Best Practices**: Proven referral strategies
• **Case Studies**: Success stories and lessons

Access all training materials in the Training Hub!`}},E=a=>{const w=a.toLowerCase();let y={score:0,response:"",sources:[]};return Object.entries(D).forEach(([k,W])=>{const G=W.keywords.reduce((V,s)=>w.includes(s)?V+1:V,0);G>y.score&&(y={score:G,response:W.content,sources:[`Knowledge Base: ${k.charAt(0).toUpperCase()+k.slice(1)}`]})}),y.score===0?{content:`I'd be happy to help! Here are some common topics I can assist with:

• **Commission & Payments** - Rates, schedules, methods
• **Referral Process** - How to submit and track referrals
• **Partnership Requirements** - Eligibility and criteria
• **Training Resources** - Guides, videos, and best practices
• **Technical Support** - Dashboard and platform help

Could you please be more specific about what you'd like to know?`,sources:["General Help"]}:{content:y.response,sources:y.sources}},z=()=>te(this,null,function*(){if(!m.trim()||N)return;const a={id:Date.now().toString(),type:"user",content:m.trim(),timestamp:new Date};o(w=>[...w,a]),b(""),f(!0),setTimeout(()=>{const w=E(a.content),y={id:(Date.now()+1).toString(),type:"ai",content:w.content,timestamp:new Date,sources:w.sources};o(k=>[...k,y]),f(!1)},1e3)}),B=a=>{a.key==="Enter"&&!a.shiftKey&&(a.preventDefault(),z())},I=(a,w)=>{o(y=>y.map(k=>k.id===a?P(C({},k),{helpful:w}):k))},i=a=>{navigator.clipboard.writeText(a)},t=()=>{o([{id:"1",type:"ai",content:"Chat cleared! How can I help you today?",timestamp:new Date,sources:[]}])};return l?e.jsxs(g.div,{initial:{opacity:0,scale:.8,y:20},animate:{opacity:1,scale:1,y:0},exit:{opacity:0,scale:.8,y:20},className:A("fixed bottom-6 right-6 z-50 w-96 bg-black border border-orange-500/20 rounded-xl shadow-2xl",v?"h-16":"h-[600px]",n),children:[e.jsx(oe,{className:"pb-3 border-b border-orange-500/20",children:e.jsxs("div",{className:"flex items-center justify-between",children:[e.jsxs("div",{className:"flex items-center space-x-3",children:[e.jsx("div",{className:"w-10 h-10 bg-gradient-to-br from-orange-500 to-red-500 rounded-full flex items-center justify-center",children:e.jsx(ie,{className:"h-5 w-5 text-white"})}),e.jsxs("div",{children:[e.jsx(le,{className:"text-sm text-white",children:"SISO AI Assistant"}),e.jsxs("div",{className:"flex items-center space-x-1",children:[e.jsx("div",{className:"w-2 h-2 bg-green-500 rounded-full"}),e.jsx("span",{className:"text-xs text-green-400",children:"Online"})]})]})]}),e.jsxs("div",{className:"flex items-center space-x-1",children:[e.jsx(h,{variant:"ghost",size:"sm",onClick:()=>S(!v),className:"h-8 w-8 p-0 text-gray-400 hover:text-white",children:v?e.jsx(Ae,{className:"h-4 w-4"}):e.jsx(Me,{className:"h-4 w-4"})}),e.jsx(h,{variant:"ghost",size:"sm",onClick:c,className:"h-8 w-8 p-0 text-gray-400 hover:text-white",children:e.jsx(Y,{className:"h-4 w-4"})})]})]})}),!v&&e.jsx(e.Fragment,{children:e.jsxs(H,{className:"p-0 h-[440px] flex flex-col",children:[e.jsx(ns,{className:"flex-1 p-4",children:e.jsxs("div",{className:"space-y-4",children:[r.map(a=>e.jsx(g.div,{initial:{opacity:0,y:10},animate:{opacity:1,y:0},className:A("flex",a.type==="user"?"justify-end":"justify-start"),children:e.jsx("div",{className:A("max-w-[80%] rounded-lg p-3 space-y-2",a.type==="user"?"bg-orange-600 text-white ml-4":"bg-gray-800 text-gray-100 mr-4"),children:e.jsxs("div",{className:"flex items-start space-x-2",children:[a.type==="ai"&&e.jsx(ee,{className:"h-4 w-4 text-orange-400 mt-0.5 flex-shrink-0"}),e.jsxs("div",{className:"flex-1",children:[e.jsx("div",{className:"text-sm whitespace-pre-wrap",children:a.content}),a.sources&&a.sources.length>0&&e.jsx("div",{className:"mt-2 space-y-1",children:a.sources.map((w,y)=>e.jsx(R,{variant:"outline",className:"text-xs",children:w},y))}),e.jsxs("div",{className:"flex items-center justify-between mt-2 text-xs text-gray-400",children:[e.jsxs("span",{className:"flex items-center space-x-1",children:[e.jsx(ne,{className:"h-3 w-3"}),e.jsx("span",{children:a.timestamp.toLocaleTimeString()})]}),a.type==="ai"&&e.jsxs("div",{className:"flex items-center space-x-1",children:[e.jsx(h,{variant:"ghost",size:"sm",onClick:()=>i(a.content),className:"h-6 w-6 p-0 text-gray-400 hover:text-white",children:e.jsx(Re,{className:"h-3 w-3"})}),e.jsx(h,{variant:"ghost",size:"sm",onClick:()=>I(a.id,!0),className:A("h-6 w-6 p-0",a.helpful===!0?"text-green-400":"text-gray-400 hover:text-green-400"),children:e.jsx(pe,{className:"h-3 w-3"})}),e.jsx(h,{variant:"ghost",size:"sm",onClick:()=>I(a.id,!1),className:A("h-6 w-6 p-0",a.helpful===!1?"text-red-400":"text-gray-400 hover:text-red-400"),children:e.jsx(Ie,{className:"h-3 w-3"})})]})]})]})]})})},a.id)),N&&e.jsx(g.div,{initial:{opacity:0,y:10},animate:{opacity:1,y:0},className:"flex justify-start",children:e.jsx("div",{className:"bg-gray-800 text-gray-100 mr-4 rounded-lg p-3",children:e.jsxs("div",{className:"flex items-center space-x-2",children:[e.jsx(me,{className:"h-4 w-4 text-orange-400 animate-spin"}),e.jsx("span",{className:"text-sm",children:"AI is thinking..."})]})})}),e.jsx("div",{ref:p})]})}),e.jsx("div",{className:"p-3 border-t border-gray-800",children:e.jsx("div",{className:"flex flex-wrap gap-1 mb-3",children:["How do commissions work?","How to submit referrals?","Payment schedule?","Training resources?"].map(a=>e.jsx(h,{variant:"outline",size:"sm",onClick:()=>b(a),className:"text-xs border-gray-600 text-gray-300 hover:bg-gray-700",children:a},a))})}),e.jsx("div",{className:"p-3 border-t border-gray-800",children:e.jsxs("div",{className:"flex space-x-2",children:[e.jsx(re,{ref:j,value:m,onChange:a=>b(a.target.value),onKeyDown:B,placeholder:"Ask about partnerships, commissions, referrals...",className:"flex-1 min-h-[40px] max-h-[100px] bg-gray-800 border-gray-600 text-white resize-none",rows:1}),e.jsxs("div",{className:"flex flex-col space-y-1",children:[e.jsx(h,{onClick:z,disabled:!m.trim()||N,className:"bg-orange-600 hover:bg-orange-700 text-white p-2",children:e.jsx(ue,{className:"h-4 w-4"})}),e.jsx(h,{variant:"outline",size:"sm",onClick:t,className:"border-gray-600 text-gray-400 hover:bg-gray-700 p-1",children:e.jsx(me,{className:"h-3 w-3"})})]})]})})]})})]}):e.jsx(g.div,{initial:{scale:0},animate:{scale:1},className:"fixed bottom-6 right-6 z-50",children:e.jsx(h,{onClick:c,className:"h-14 w-14 rounded-full bg-orange-600 hover:bg-orange-700 shadow-lg",children:e.jsx(se,{className:"h-6 w-6 text-white"})})})}function ms({isOpen:l,onClose:c,onSubmit:n}){var I,i;const[r,o]=u.useState({category:"",priority:"medium",subject:"",description:"",contactMethod:"email",clientAffected:"",dealValue:"",urgentReason:"",attachments:[],requestCallback:!1,anonymousSubmission:!1}),[m,b]=u.useState([]),[N,f]=u.useState(!1),[v,S]=u.useState(1),p=[{value:"technical",label:"Technical Support",icon:"🔧",description:"Platform issues, bugs, portal problems"},{value:"commission",label:"Commission & Payments",icon:"💰",description:"Payment issues, commission questions"},{value:"referral",label:"Referral Support",icon:"👥",description:"Client referral assistance, tracking issues"},{value:"training",label:"Training & Education",icon:"📚",description:"Learning resources, best practices"},{value:"account",label:"Account Management",icon:"👤",description:"Profile updates, access issues"},{value:"marketing",label:"Marketing Materials",icon:"📢",description:"Brochures, templates, co-marketing"},{value:"urgent",label:"Urgent Business Issue",icon:"🚨",description:"Time-sensitive deal or client matters"},{value:"feedback",label:"Feedback & Suggestions",icon:"💡",description:"Product feedback, feature requests"}],j=[{value:"low",label:"Low Priority",color:"bg-blue-500",description:"General questions, non-urgent matters"},{value:"medium",label:"Medium Priority",color:"bg-yellow-500",description:"Important but not time-critical"},{value:"high",label:"High Priority",color:"bg-orange-500",description:"Urgent issues affecting business"},{value:"critical",label:"Critical",color:"bg-red-500",description:"Emergency - immediate attention required"}],U=t=>{Array.from(t.target.files||[]).forEach(w=>{if(w.size>10*1024*1024){alert(`File ${w.name} is too large. Maximum size is 10MB.`);return}const y={file:w,type:w.type.startsWith("image/")?"image":w.type.includes("pdf")||w.type.includes("document")?"document":"other"};if(y.type==="image"){const k=new FileReader;k.onload=W=>{var G;y.preview=(G=W.target)==null?void 0:G.result,b(V=>[...V,y])},k.readAsDataURL(w)}else b(k=>[...k,y]);o(k=>P(C({},k),{attachments:[...k.attachments,w]}))}),t.target.value=""},D=t=>{b(a=>a.filter((w,y)=>y!==t)),o(a=>P(C({},a),{attachments:a.attachments.filter((w,y)=>y!==t)}))},E=()=>te(this,null,function*(){f(!0),yield new Promise(a=>setTimeout(a,2e3));const t=`TICKET-${Date.now()}`;console.log("Support ticket submitted:",P(C({},r),{ticketId:t})),n&&n(r),f(!1),c(),alert(`Support ticket ${t} submitted successfully! You'll receive a confirmation email shortly.`)}),z=()=>r.category&&r.subject&&r.description.length>=20,B=()=>{switch(r.priority){case"critical":return"< 1 hour";case"high":return"< 4 hours";case"medium":return"< 24 hours";case"low":return"< 48 hours";default:return"< 24 hours"}};return l?e.jsx(g.div,{initial:{opacity:0},animate:{opacity:1},exit:{opacity:0},className:"fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4",onClick:t=>t.target===t.currentTarget&&c(),children:e.jsx(g.div,{initial:{scale:.9,opacity:0},animate:{scale:1,opacity:1},exit:{scale:.9,opacity:0},className:"w-full max-w-4xl max-h-[90vh] overflow-y-auto",children:e.jsxs(F,{className:"bg-black border-orange-500/20",children:[e.jsxs(oe,{className:"border-b border-orange-500/20",children:[e.jsxs("div",{className:"flex items-center justify-between",children:[e.jsxs("div",{children:[e.jsxs(le,{className:"text-xl text-white flex items-center",children:[e.jsx(De,{className:"h-6 w-6 mr-2 text-orange-500"}),"Create Support Ticket"]}),e.jsx("p",{className:"text-gray-400 mt-1",children:"Get help from our partnership specialists - we're here to support your success"})]}),e.jsx(h,{variant:"ghost",size:"sm",onClick:c,className:"text-gray-400 hover:text-white",children:e.jsx(Y,{className:"h-5 w-5"})})]}),e.jsx("div",{className:"flex items-center space-x-4 mt-4",children:[1,2,3].map(t=>e.jsxs("div",{className:"flex items-center",children:[e.jsx("div",{className:A("w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium",v>=t?"bg-orange-500 text-white":"bg-gray-700 text-gray-400"),children:t}),t<3&&e.jsx("div",{className:A("w-12 h-0.5 mx-2",v>t?"bg-orange-500":"bg-gray-700")})]},t))})]}),e.jsxs(H,{className:"p-6",children:[v===1&&e.jsxs(g.div,{initial:{opacity:0,x:20},animate:{opacity:1,x:0},className:"space-y-6",children:[e.jsxs("div",{children:[e.jsx(T,{className:"text-white text-lg mb-4 block",children:"What type of support do you need?"}),e.jsx("div",{className:"grid grid-cols-1 md:grid-cols-2 gap-4",children:p.map(t=>e.jsx("div",{onClick:()=>o(a=>P(C({},a),{category:t.value})),className:A("p-4 rounded-lg border cursor-pointer transition-all",r.category===t.value?"border-orange-500 bg-orange-500/10":"border-gray-700 hover:border-gray-600 bg-gray-900/50"),children:e.jsxs("div",{className:"flex items-start space-x-3",children:[e.jsx("span",{className:"text-2xl",children:t.icon}),e.jsxs("div",{children:[e.jsx("h3",{className:"text-white font-medium",children:t.label}),e.jsx("p",{className:"text-gray-400 text-sm mt-1",children:t.description})]})]})},t.value))})]}),e.jsxs("div",{children:[e.jsx(T,{className:"text-white text-lg mb-4 block",children:"Priority Level"}),e.jsx(os,{value:r.priority,onValueChange:t=>o(a=>P(C({},a),{priority:t})),children:e.jsx("div",{className:"grid grid-cols-1 md:grid-cols-2 gap-4",children:j.map(t=>e.jsxs("div",{className:"flex items-start space-x-3",children:[e.jsx(ls,{value:t.value,id:t.value,className:"mt-1"}),e.jsx(T,{htmlFor:t.value,className:"flex-1 cursor-pointer",children:e.jsxs("div",{className:"flex items-center space-x-3",children:[e.jsx("div",{className:A("w-3 h-3 rounded-full",t.color)}),e.jsxs("div",{children:[e.jsx("div",{className:"text-white font-medium",children:t.label}),e.jsx("div",{className:"text-gray-400 text-sm",children:t.description}),e.jsxs("div",{className:"text-orange-400 text-xs mt-1",children:["Expected response: ",B()]})]})]})})]},t.value))})})]}),e.jsx("div",{className:"flex justify-end",children:e.jsx(h,{onClick:()=>S(2),disabled:!r.category,className:"bg-orange-600 hover:bg-orange-700",children:"Next Step"})})]}),v===2&&e.jsxs(g.div,{initial:{opacity:0,x:20},animate:{opacity:1,x:0},className:"space-y-6",children:[e.jsxs("div",{className:"grid grid-cols-1 md:grid-cols-2 gap-6",children:[e.jsxs("div",{children:[e.jsx(T,{htmlFor:"subject",className:"text-white",children:"Subject *"}),e.jsx(Q,{id:"subject",value:r.subject,onChange:t=>o(a=>P(C({},a),{subject:t.target.value})),placeholder:"Brief description of your issue",className:"bg-gray-800 border-gray-600 text-white mt-2"})]}),e.jsxs("div",{children:[e.jsx(T,{htmlFor:"contactMethod",className:"text-white",children:"Preferred Contact Method"}),e.jsxs(xe,{value:r.contactMethod,onValueChange:t=>o(a=>P(C({},a),{contactMethod:t})),children:[e.jsx(fe,{className:"bg-gray-800 border-gray-600 text-white mt-2",children:e.jsx(ye,{})}),e.jsxs(be,{children:[e.jsx(O,{value:"email",children:"Email"}),e.jsx(O,{value:"phone",children:"Phone Call"}),e.jsx(O,{value:"video",children:"Video Call"}),e.jsx(O,{value:"chat",children:"Live Chat"})]})]})]})]}),r.category==="urgent"&&e.jsxs("div",{className:"grid grid-cols-1 md:grid-cols-2 gap-6",children:[e.jsxs("div",{children:[e.jsx(T,{htmlFor:"clientAffected",className:"text-white",children:"Client/Deal Affected"}),e.jsx(Q,{id:"clientAffected",value:r.clientAffected,onChange:t=>o(a=>P(C({},a),{clientAffected:t.target.value})),placeholder:"Client name or deal reference",className:"bg-gray-800 border-gray-600 text-white mt-2"})]}),e.jsxs("div",{children:[e.jsx(T,{htmlFor:"dealValue",className:"text-white",children:"Potential Deal Value"}),e.jsx(Q,{id:"dealValue",value:r.dealValue,onChange:t=>o(a=>P(C({},a),{dealValue:t.target.value})),placeholder:"£10,000",className:"bg-gray-800 border-gray-600 text-white mt-2"})]})]}),e.jsxs("div",{children:[e.jsx(T,{htmlFor:"description",className:"text-white",children:"Detailed Description *"}),e.jsx(re,{id:"description",value:r.description,onChange:t=>o(a=>P(C({},a),{description:t.target.value})),placeholder:"Please provide as much detail as possible about your issue, including steps to reproduce, error messages, or specific questions...",className:"bg-gray-800 border-gray-600 text-white mt-2 min-h-[120px]"}),e.jsxs("p",{className:"text-gray-400 text-sm mt-1",children:[r.description.length,"/20 characters minimum"]})]}),r.priority==="critical"&&e.jsxs("div",{children:[e.jsx(T,{htmlFor:"urgentReason",className:"text-white",children:"Why is this critical? *"}),e.jsx(re,{id:"urgentReason",value:r.urgentReason,onChange:t=>o(a=>P(C({},a),{urgentReason:t.target.value})),placeholder:"Explain the business impact and timeline...",className:"bg-gray-800 border-gray-600 text-white mt-2"})]}),e.jsxs("div",{className:"flex items-center space-x-4",children:[e.jsx(h,{onClick:()=>S(1),variant:"outline",className:"border-gray-600",children:"Back"}),e.jsx(h,{onClick:()=>S(3),disabled:!r.subject||r.description.length<20,className:"bg-orange-600 hover:bg-orange-700",children:"Next Step"})]})]}),v===3&&e.jsxs(g.div,{initial:{opacity:0,x:20},animate:{opacity:1,x:0},className:"space-y-6",children:[e.jsxs("div",{children:[e.jsx(T,{className:"text-white text-lg mb-4 block",children:"Attachments (Optional)"}),e.jsxs("div",{className:"border-2 border-dashed border-gray-600 rounded-lg p-6 text-center",children:[e.jsx("input",{type:"file",id:"file-upload",multiple:!0,accept:".pdf,.doc,.docx,.txt,.png,.jpg,.jpeg,.gif,.zip",onChange:U,className:"hidden"}),e.jsxs(T,{htmlFor:"file-upload",className:"cursor-pointer",children:[e.jsx(Be,{className:"h-12 w-12 text-gray-400 mx-auto mb-4"}),e.jsx("p",{className:"text-white mb-2",children:"Click to upload or drag and drop"}),e.jsx("p",{className:"text-gray-400 text-sm",children:"Supports: PDF, DOC, TXT, Images, ZIP (Max 10MB each)"})]})]}),m.length>0&&e.jsx("div",{className:"grid grid-cols-2 md:grid-cols-4 gap-4 mt-4",children:m.map((t,a)=>e.jsxs("div",{className:"relative bg-gray-800 rounded-lg p-3",children:[e.jsxs("div",{className:"flex items-center justify-between mb-2",children:[e.jsx("div",{className:"text-white text-sm truncate",children:t.file.name}),e.jsx(h,{variant:"ghost",size:"sm",onClick:()=>D(a),className:"h-6 w-6 p-0 text-gray-400 hover:text-red-400",children:e.jsx(Y,{className:"h-4 w-4"})})]}),t.type==="image"&&t.preview?e.jsx("img",{src:t.preview,alt:t.file.name,className:"w-full h-16 object-cover rounded"}):e.jsx("div",{className:"w-full h-16 bg-gray-700 rounded flex items-center justify-center",children:t.type==="document"?e.jsx(J,{className:"h-8 w-8 text-blue-400"}):e.jsx(qe,{className:"h-8 w-8 text-gray-400"})}),e.jsxs("p",{className:"text-gray-400 text-xs mt-1",children:[(t.file.size/1024/1024).toFixed(1)," MB"]})]},a))})]}),e.jsxs("div",{className:"space-y-4",children:[e.jsxs("div",{className:"flex items-center space-x-2",children:[e.jsx(Z,{id:"callback",checked:r.requestCallback,onCheckedChange:t=>o(a=>P(C({},a),{requestCallback:t}))}),e.jsx(T,{htmlFor:"callback",className:"text-white",children:"Request a callback for this issue"})]}),e.jsxs("div",{className:"flex items-center space-x-2",children:[e.jsx(Z,{id:"anonymous",checked:r.anonymousSubmission,onCheckedChange:t=>o(a=>P(C({},a),{anonymousSubmission:t}))}),e.jsx(T,{htmlFor:"anonymous",className:"text-white",children:"Submit anonymously (for sensitive feedback)"})]})]}),e.jsxs("div",{className:"bg-gray-900 rounded-lg p-4",children:[e.jsx("h3",{className:"text-white font-medium mb-3",children:"Ticket Summary"}),e.jsxs("div",{className:"space-y-2 text-sm",children:[e.jsxs("div",{className:"flex justify-between",children:[e.jsx("span",{className:"text-gray-400",children:"Category:"}),e.jsx("span",{className:"text-white",children:(I=p.find(t=>t.value===r.category))==null?void 0:I.label})]}),e.jsxs("div",{className:"flex justify-between",children:[e.jsx("span",{className:"text-gray-400",children:"Priority:"}),e.jsx(R,{variant:"outline",className:A("text-white",r.priority==="critical"?"border-red-500":r.priority==="high"?"border-orange-500":r.priority==="medium"?"border-yellow-500":"border-blue-500"),children:(i=j.find(t=>t.value===r.priority))==null?void 0:i.label})]}),e.jsxs("div",{className:"flex justify-between",children:[e.jsx("span",{className:"text-gray-400",children:"Expected Response:"}),e.jsx("span",{className:"text-orange-400",children:B()})]}),e.jsxs("div",{className:"flex justify-between",children:[e.jsx("span",{className:"text-gray-400",children:"Attachments:"}),e.jsxs("span",{className:"text-white",children:[r.attachments.length," files"]})]})]})]}),e.jsxs("div",{className:"flex items-center space-x-4",children:[e.jsx(h,{onClick:()=>S(2),variant:"outline",className:"border-gray-600",children:"Back"}),e.jsx(h,{onClick:E,disabled:!z()||N,className:"bg-orange-600 hover:bg-orange-700 flex-1",children:N?e.jsxs(e.Fragment,{children:[e.jsx(ne,{className:"h-4 w-4 mr-2 animate-spin"}),"Submitting Ticket..."]}):e.jsxs(e.Fragment,{children:[e.jsx(ue,{className:"h-4 w-4 mr-2"}),"Submit Support Ticket"]})})]})]})]})]})})}):null}function ps({onSearchClick:l,onAIAssistantClick:c,className:n}){const[r,o]=u.useState(""),[m,b]=u.useState(!1),N=[{text:"How to submit referrals",trend:"up",searches:234},{text:"Commission rates",trend:"up",searches:189},{text:"Payment schedule",trend:"stable",searches:156},{text:"Partnership requirements",trend:"up",searches:143},{text:"Training materials",trend:"up",searches:98},{text:"API documentation",trend:"stable",searches:67}],f=[{title:"AI Assistant",description:"Get instant answers from our AI",icon:ie,color:"bg-purple-500/20 text-purple-400 border-purple-500/30",action:c},{title:"Advanced Search",description:"Detailed search with filters",icon:$,color:"bg-blue-500/20 text-blue-400 border-blue-500/30",action:l}],v=()=>{r.trim()&&(l==null||l())},S=p=>{p.key==="Enter"&&v()};return e.jsxs("div",{className:A("space-y-8",n),children:[e.jsx(g.div,{initial:{opacity:0,y:20},animate:{opacity:1,y:0},className:"text-center space-y-6",children:e.jsxs("div",{className:"relative max-w-2xl mx-auto",children:[e.jsx("div",{className:"absolute inset-0 bg-gradient-to-r from-orange-500/20 to-red-500/20 rounded-2xl blur-xl"}),e.jsxs("div",{className:"relative bg-black/30 backdrop-blur-sm border border-orange-500/20 rounded-2xl p-8",children:[e.jsxs(g.div,{initial:{scale:.8},animate:{scale:1},transition:{delay:.2},className:"mb-6",children:[e.jsx(ee,{className:"h-12 w-12 text-orange-400 mx-auto mb-4"}),e.jsx("h2",{className:"text-2xl font-bold text-white mb-2",children:"How can we help you?"}),e.jsx("p",{className:"text-gray-300",children:"Search our knowledge base or chat with our AI assistant"})]}),e.jsxs("div",{className:"relative mb-6",children:[e.jsxs("div",{className:"relative",children:[e.jsx($,{className:"absolute left-4 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400"}),e.jsx(Q,{value:r,onChange:p=>o(p.target.value),onKeyDown:S,onFocus:()=>b(!0),onBlur:()=>setTimeout(()=>b(!1),200),placeholder:"Search for help articles, guides, FAQs...",className:"pl-12 pr-12 h-14 text-lg bg-gray-800/50 border-gray-600 text-white rounded-xl"}),e.jsx(h,{onClick:v,className:"absolute right-2 top-1/2 transform -translate-y-1/2 bg-orange-600 hover:bg-orange-700 rounded-lg",children:e.jsx(_,{className:"h-4 w-4"})})]}),e.jsx(X,{children:m&&e.jsx(g.div,{initial:{opacity:0,y:-10},animate:{opacity:1,y:0},exit:{opacity:0,y:-10},className:"absolute top-full left-0 right-0 mt-2 bg-gray-800 border border-gray-600 rounded-xl shadow-xl z-50",children:e.jsxs("div",{className:"p-4",children:[e.jsxs("h4",{className:"text-white font-medium mb-3 flex items-center",children:[e.jsx(ae,{className:"h-4 w-4 mr-2 text-orange-400"}),"Popular Searches"]}),e.jsx("div",{className:"space-y-2",children:N.slice(0,4).map((p,j)=>e.jsxs("button",{onClick:()=>{o(p.text),b(!1)},className:"w-full text-left flex items-center justify-between p-2 rounded-lg hover:bg-gray-700 transition-colors group",children:[e.jsx("span",{className:"text-gray-300 group-hover:text-white",children:p.text}),e.jsxs("div",{className:"flex items-center space-x-2",children:[e.jsx(R,{variant:"outline",className:"text-xs",children:p.searches}),e.jsx(ae,{className:A("h-3 w-3",p.trend==="up"?"text-green-400":"text-gray-400")})]})]},j))})]})})})]}),e.jsx("div",{className:"grid grid-cols-1 md:grid-cols-2 gap-4",children:f.map((p,j)=>e.jsx(g.button,{initial:{opacity:0,scale:.9},animate:{opacity:1,scale:1},transition:{delay:.3+j*.1},onClick:p.action,className:A("p-4 rounded-xl border transition-all hover:scale-105 text-left",p.color),children:e.jsxs("div",{className:"flex items-center space-x-3",children:[e.jsx(p.icon,{className:"h-8 w-8"}),e.jsxs("div",{children:[e.jsx("h3",{className:"font-medium",children:p.title}),e.jsx("p",{className:"text-sm opacity-80",children:p.description})]})]})},j))})]})]})}),e.jsx(g.div,{initial:{opacity:0,y:20},animate:{opacity:1,y:0},transition:{delay:.4},className:"max-w-4xl mx-auto",children:e.jsx(F,{className:"bg-gray-800/50 border-gray-600",children:e.jsxs(H,{className:"p-6",children:[e.jsxs("div",{className:"flex items-center justify-between mb-4",children:[e.jsxs("h3",{className:"text-white font-medium flex items-center",children:[e.jsx(ne,{className:"h-5 w-5 mr-2 text-orange-400"}),"Trending Topics"]}),e.jsx(h,{variant:"ghost",size:"sm",onClick:l,className:"text-orange-400 hover:text-orange-300",children:"View All"})]}),e.jsx("div",{className:"grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4",children:N.map((p,j)=>e.jsxs(g.button,{initial:{opacity:0,x:-20},animate:{opacity:1,x:0},transition:{delay:.5+j*.05},onClick:()=>{o(p.text),l==null||l()},className:"text-left p-3 rounded-lg bg-gray-700/50 hover:bg-gray-700 transition-all group",children:[e.jsxs("div",{className:"flex items-center justify-between mb-2",children:[e.jsx("span",{className:"text-white text-sm font-medium group-hover:text-orange-400 transition-colors",children:p.text}),e.jsx(_,{className:"h-3 w-3 text-gray-400 group-hover:text-orange-400 transition-colors"})]}),e.jsxs("div",{className:"flex items-center space-x-2",children:[e.jsxs(R,{variant:"outline",className:"text-xs",children:[p.searches," searches"]}),p.trend==="up"&&e.jsxs("div",{className:"flex items-center space-x-1",children:[e.jsx(ae,{className:"h-3 w-3 text-green-400"}),e.jsx("span",{className:"text-xs text-green-400",children:"Trending"})]})]})]},j))})]})})}),e.jsx(g.div,{initial:{opacity:0,y:20},animate:{opacity:1,y:0},transition:{delay:.6},className:"max-w-3xl mx-auto",children:e.jsx(F,{className:"bg-gradient-to-r from-purple-900/20 to-blue-900/20 border-purple-500/20",children:e.jsx(H,{className:"p-6",children:e.jsxs("div",{className:"flex items-center justify-between",children:[e.jsxs("div",{className:"flex items-center space-x-4",children:[e.jsx("div",{className:"w-12 h-12 bg-purple-500/20 rounded-xl flex items-center justify-center",children:e.jsx(ie,{className:"h-6 w-6 text-purple-400"})}),e.jsxs("div",{children:[e.jsx("h3",{className:"text-white font-medium mb-1",children:"Can't find what you're looking for?"}),e.jsx("p",{className:"text-gray-300 text-sm",children:"Our AI assistant can help you find answers instantly and guide you through any process"})]})]}),e.jsxs(h,{onClick:c,className:"bg-purple-600 hover:bg-purple-700 text-white",children:[e.jsx(he,{className:"h-4 w-4 mr-2"}),"Ask AI"]})]})})})})]})}const ve=[{id:"complete-partnership-guide",title:"Complete Partnership Success Guide",description:"Your comprehensive roadmap to maximizing earnings and building successful long-term partnerships with SISO. From first referral to top-tier status.",category:"Getting Started",readTime:"12 min read",imageUrl:"/images/partnership-success-guide.jpg",link:"/partner/training-hub/complete-guide",author:"Sarah Mitchell, Partnership Director",publishedDate:"2024-01-15",tags:["partnership","success","strategy","earnings"]},{id:"referral-mastery-blueprint",title:"Referral Mastery Blueprint",description:"Proven strategies and tactics used by our top-earning partners to consistently generate high-quality referrals and maximize conversion rates.",category:"Best Practices",readTime:"15 min read",imageUrl:"/images/referral-mastery.jpg",link:"/partner/training-hub/referral-blueprint",author:"Marcus Chen, Top Partner",publishedDate:"2024-01-12",tags:["referrals","conversion","strategy","networking"]},{id:"commission-optimization",title:"Commission Structure & Optimization",description:"Deep dive into our commission system, tier benefits, bonus opportunities, and strategies to maximize your earnings potential with SISO.",category:"Financial",readTime:"10 min read",imageUrl:"/images/commission-guide.jpg",link:"/partner/training-hub/commission-guide",author:"Finance Team",publishedDate:"2024-01-10",tags:["commission","payments","optimization","tiers"]},{id:"client-relationship-management",title:"Client Relationship Excellence",description:"How to build trust, manage expectations, and maintain long-term relationships that lead to repeat business and referrals.",category:"Relationship Building",readTime:"8 min read",imageUrl:"/images/client-relationships.jpg",link:"/partner/training-hub/client-relations",author:"Emma Rodriguez, Client Success",publishedDate:"2024-01-08",tags:["clients","relationships","trust","communication"]}],us=[{id:"live-chat",title:"Live Chat Support",description:"Connect instantly with our partnership specialists for real-time assistance with any questions or issues.",icon:se,status:"online",action:()=>{typeof window!="undefined"&&window.Intercom?window.Intercom("show"):console.log("Opening live chat...")},actionText:"Start Chat",responseTime:"< 2 minutes",availability:"Mon-Fri 9AM-6PM GMT, Sat 10AM-4PM GMT"},{id:"email-support",title:"Email Support",description:"Send detailed questions, feedback, or requests to our dedicated partnership support team.",icon:We,status:"available",action:()=>{window.open("mailto:partners@siso.agency?subject=Partnership Support Request&body=Hi SISO Team,%0D%0A%0D%0AI need assistance with:%0D%0A%0D%0A[Please describe your question or issue]%0D%0A%0D%0APartner ID: [Your Partner ID]%0D%0AUrgency: [Low/Medium/High]%0D%0A%0D%0AThank you!","_blank")},actionText:"Send Email",responseTime:"< 4 hours",availability:"24/7 - We respond during business hours"},{id:"phone-support",title:"Phone Support",description:"Schedule a call or speak directly with our partnership experts for complex issues or strategy discussions.",icon:Ve,status:"available",action:()=>{window.open("https://calendly.com/siso-partnership/support-call","_blank")},actionText:"Schedule Call",responseTime:"Same day",availability:"Mon-Fri 9AM-6PM GMT"},{id:"emergency-support",title:"Emergency Support",description:"For urgent issues affecting active deals or time-sensitive matters requiring immediate attention.",icon:he,status:"available",action:()=>{window.open("mailto:urgent@siso.agency?subject=URGENT: Partnership Emergency&body=URGENT PARTNERSHIP ISSUE%0D%0A%0D%0ANature of Emergency:%0D%0A%0D%0AClient/Deal Affected:%0D%0A%0D%0ATimeline:%0D%0A%0D%0AContact Number:%0D%0A%0D%0ADetails:","_blank")},actionText:"Report Issue",responseTime:"< 1 hour",availability:"24/7 for genuine emergencies"},{id:"training-hub",title:"Training Hub",description:"Access comprehensive training materials, video tutorials, and self-paced learning resources.",icon:ge,status:"available",action:()=>{window.location.href="/partner/training-hub"},actionText:"View Training",responseTime:"Instant access",availability:"24/7 self-service"},{id:"community-forum",title:"Partner Community",description:"Connect with other partners, share experiences, and get advice from successful partnership veterans.",icon:Qe,status:"available",action:()=>{window.open("https://community.siso.agency/partners","_blank")},actionText:"Join Community",responseTime:"Community-driven",availability:"24/7 peer support"}],je=[{id:"partnership-handbook",title:"Complete Partnership Handbook",description:"Comprehensive 150-page guide covering every aspect of the SISO partnership program, from onboarding to advanced strategies.",icon:ge,category:"Documentation",downloadUrl:"/downloads/siso-partnership-handbook-2024.pdf",fileSize:"15.2 MB",rating:4.9,lastUpdated:"2024-01-15",downloads:2847},{id:"commission-calculator",title:"Commission Calculator Tool",description:"Interactive Excel spreadsheet to calculate potential earnings, track performance, and plan your partnership growth.",icon:Ee,category:"Tools",downloadUrl:"/downloads/siso-commission-calculator.xlsx",fileSize:"2.8 MB",rating:4.8,lastUpdated:"2024-01-12",downloads:1923},{id:"training-video-library",title:"Complete Video Training Library",description:"Over 50 professional training videos covering all aspects of partnership success, recorded by industry experts.",icon:ze,category:"Training",downloadUrl:"/partner/training-hub/video-library",fileSize:"85 videos",rating:4.9,lastUpdated:"2024-01-14",downloads:3156},{id:"marketing-materials-kit",title:"Professional Marketing Materials",description:"Ready-to-use presentation templates, brochures, case studies, and promotional materials for client meetings.",icon:Le,category:"Marketing",downloadUrl:"/downloads/siso-marketing-kit-2024.zip",fileSize:"28.5 MB",rating:4.7,lastUpdated:"2024-01-10",downloads:1654},{id:"client-proposal-templates",title:"Client Proposal Templates",description:"Professional proposal templates for different service types, with customizable sections and proven conversion rates.",icon:J,category:"Templates",downloadUrl:"/downloads/siso-proposal-templates.zip",fileSize:"12.3 MB",rating:4.8,lastUpdated:"2024-01-08",downloads:2234},{id:"api-documentation",title:"Partner API Documentation",description:"Technical documentation for integrating with SISO systems, tracking APIs, and automated reporting tools.",icon:Oe,category:"Technical",downloadUrl:"/partner/api-documentation",fileSize:"Online docs",rating:4.6,lastUpdated:"2024-01-13",downloads:456},{id:"legal-documents",title:"Legal Documents & Agreements",description:"Partnership agreements, terms of service, privacy policies, and legal frameworks governing the partnership.",icon:He,category:"Legal",downloadUrl:"/downloads/siso-legal-documents.pdf",fileSize:"8.7 MB",rating:4.5,lastUpdated:"2024-01-05",downloads:1876},{id:"success-case-studies",title:"Partner Success Case Studies",description:"Real success stories from top-performing partners, including strategies, challenges overcome, and earnings achieved.",icon:Ge,category:"Inspiration",downloadUrl:"/downloads/siso-case-studies-2024.pdf",fileSize:"18.9 MB",rating:4.9,lastUpdated:"2024-01-11",downloads:2987}],we=[{id:"getting-started",title:"Getting Started",description:"Everything you need to begin your partnership journey successfully",icon:Fe,color:"green",articles:[{id:"partnership-requirements",title:"Partnership Requirements & Eligibility",summary:"Understand the criteria and qualifications needed to become a SISO partner",content:`# Partnership Requirements & Eligibility

## Who Can Become a SISO Partner?

### **Professional Background Requirements:**
- **Business Network**: Active connections in the business, technology, or entrepreneurship space
- **Communication Skills**: Ability to articulate value propositions and build relationships
- **Professional Reputation**: Established credibility in your industry or market
- **Commitment Level**: Willingness to actively promote and support SISO services

### **No Barriers to Entry:**
- **No upfront costs** or joining fees
- **No minimum commitment** requirements
- **No exclusive arrangements** - work with other agencies if desired
- **No geographic restrictions** - global partnership opportunities

### **Ideal Partner Profiles:**
- **Business Consultants** and advisors
- **Technology Professionals** and developers
- **Marketing Agencies** and freelancers
- **Startup Advisors** and accelerator networks
- **Industry Specialists** with relevant client bases

### **Application Process:**
1. **Complete the partnership application** (5-10 minutes)
2. **Brief qualification call** with our partnership team
3. **Review partnership agreement** and terms
4. **Access to partner portal** and resources
5. **Start referring clients** immediately

### **What We Look For:**
- **Quality over Quantity**: We prefer partners who focus on high-quality referrals
- **Client-First Mindset**: Genuine interest in helping clients succeed
- **Professional Approach**: Reliable communication and follow-through
- **Growth Potential**: Ability to scale referral activities over time

**Ready to apply?** Contact partners@siso.agency or use the partnership application form.`,lastUpdated:"2024-01-15",views:1247,helpful:98,tags:["eligibility","requirements","application","getting-started"]},{id:"first-referral-guide",title:"How to Submit Your First Referral",summary:"Step-by-step guide to making your first successful client referral",content:`# How to Submit Your First Referral

## Step-by-Step Process

### **Step 1: Identify a Potential Client**
- Look for businesses needing digital transformation
- Consider companies with growth ambitions
- Focus on clients with budgets above £5,000
- Prioritize warm connections and existing relationships

### **Step 2: Qualify the Opportunity**
Use our **BANT qualification framework:**
- **Budget**: Does the client have adequate budget?
- **Authority**: Are you speaking with decision-makers?
- **Need**: Is there a clear business need for our services?
- **Timeline**: Is there a reasonable timeline for implementation?

### **Step 3: Complete Your Partner Profile**
Before submitting referrals, ensure your profile includes:
- Complete contact information
- Professional background summary
- Areas of expertise and industry focus
- Payment details for commission processing

### **Step 4: Gather Client Information**
Required information for referral submission:
- **Company Details**: Name, size, industry, website
- **Contact Information**: Primary contact name, email, phone
- **Project Scope**: Services needed, approximate budget
- **Timeline**: When they want to start
- **Background**: How you know them, their specific challenges

### **Step 5: Submit Through Partner Portal**
1. Log into your partner dashboard
2. Navigate to "New Referral" section
3. Complete the referral form with all details
4. Add any relevant notes or context
5. Submit for review

### **Step 6: Follow Up**
- **Initial Follow-up**: Contact client within 24 hours
- **Introduce SISO**: Warm introduction via email or call
- **Stay Engaged**: Monitor progress and provide support
- **Track Progress**: Use partner dashboard to monitor status

### **Best Practices for First Referrals:**
- Start with your strongest relationships
- Be transparent about the partnership
- Focus on the client's needs, not your commission
- Provide context and background to SISO team
- Follow up consistently but not aggressively

### **What Happens Next:**
1. **Review Process**: SISO team reviews referral within 24 hours
2. **Initial Contact**: We reach out to the client within 48 hours
3. **Discovery Call**: Detailed needs assessment and proposal development
4. **Proposal Delivery**: Custom proposal based on requirements
5. **Commission Tracking**: Real-time updates in your dashboard

**Need help with your first referral?** Contact our partnership team for personalized guidance.`,lastUpdated:"2024-01-14",views:892,helpful:87,tags:["first-referral","process","guide","qualification"]},{id:"partner-portal-setup",title:"Setting Up Your Partner Portal",summary:"Complete guide to configuring your partner dashboard and account settings",content:`# Setting Up Your Partner Portal

## Initial Account Setup

### **Accessing Your Portal**
- **URL**: https://partners.siso.agency
- **Login**: Use the credentials sent to your email
- **Two-Factor Authentication**: Highly recommended for security

### **Profile Configuration**

#### **Personal Information:**
- Full name and professional title
- Contact information (email, phone, address)
- Professional headshot (optional but recommended)
- LinkedIn profile and social media links

#### **Business Information:**
- Company name and description
- Industry focus and expertise areas
- Target client demographics
- Geographic coverage areas

#### **Banking Details:**
- Preferred payment method (bank transfer, PayPal, Wise)
- Account details for commission payments
- Tax information and VAT registration (if applicable)
- Invoice preferences and billing address

### **Dashboard Overview**

#### **Key Sections:**
1. **Referral Management**: Submit, track, and manage all referrals
2. **Commission Tracking**: Real-time earnings and payment history
3. **Performance Analytics**: Detailed metrics and insights
4. **Training Resources**: Access to all learning materials
5. **Support Center**: Direct access to help and assistance

#### **Customization Options:**
- **Notification Preferences**: Email alerts for updates
- **Dashboard Layout**: Arrange widgets according to preference
- **Reporting Frequency**: Daily, weekly, or monthly summaries
- **Privacy Settings**: Control information sharing

### **Referral Link Generation**
- **Unique Tracking Links**: Automatically generated for each partner
- **Custom UTM Parameters**: Track traffic sources and campaigns
- **QR Code Generation**: For offline marketing materials
- **Link Analytics**: Click tracking and conversion metrics

### **Mobile App Setup**
- **Download**: Available for iOS and Android
- **Push Notifications**: Real-time referral updates
- **Offline Access**: View cached data without internet
- **Quick Actions**: Submit referrals on the go

### **Security Best Practices**
- Enable two-factor authentication
- Use strong, unique passwords
- Regular security reviews
- Report suspicious activity immediately

### **Getting Help**
- **In-Portal Support**: Live chat widget available 24/7
- **Knowledge Base**: Searchable help articles
- **Video Tutorials**: Step-by-step setup guides
- **Personal Onboarding**: Schedule a setup call if needed

**Having trouble with setup?** Our technical support team is available to help with any configuration issues.`,lastUpdated:"2024-01-13",views:743,helpful:92,tags:["portal","setup","configuration","dashboard"]},{id:"partnership-tiers-benefits",title:"Partnership Tiers & Benefits",summary:"Understanding the different partnership levels and their unique benefits",content:`# Partnership Tiers & Benefits

## Tier Structure Overview

### **Bronze Partner** (Entry Level)
**Qualification:** 0-5 successful referrals

#### **Benefits:**
- **Commission Rate**: 15% on all approved projects
- **Payment Schedule**: Monthly (minimum £100)
- **Access Level**: Basic training materials and portal
- **Support**: Email and chat support during business hours
- **Marketing Materials**: Standard templates and brochures

#### **Requirements:**
- Complete partner profile
- Agree to partnership terms
- Submit at least one referral per quarter

---

### **Silver Partner** (Established)
**Qualification:** 6-15 successful referrals OR £10K+ in commissions

#### **Benefits:**
- **Commission Rate**: 18% on all approved projects
- **Payment Schedule**: Bi-weekly (minimum £50)
- **Access Level**: Advanced training resources
- **Support**: Priority support with faster response times
- **Marketing Materials**: Customizable templates and co-branded materials
- **Bonus Opportunities**: Quarterly performance bonuses
- **Networking Events**: Invitation to partner meetups and webinars

#### **Additional Perks:**
- Dedicated account manager
- Early access to new services
- Client feedback and case study participation

---

### **Gold Partner** (Expert Level)
**Qualification:** 16-30 successful referrals OR £25K+ in commissions

#### **Benefits:**
- **Commission Rate**: 22% on all approved projects
- **Payment Schedule**: Weekly (no minimum)
- **Access Level**: Premium training and exclusive resources
- **Support**: Dedicated support hotline and personal account manager
- **Marketing Materials**: Fully customized materials and direct mail campaigns
- **Bonus Opportunities**: Monthly bonuses plus annual incentive trips
- **Client Collaboration**: Joint proposal development and client meetings

#### **Additional Perks:**
- Revenue sharing on long-term clients
- Co-marketing opportunities
- Speaking opportunities at events
- Access to beta services and features

---

### **Platinum Partner** (Strategic Alliance)
**Qualification:** 31+ successful referrals OR £50K+ in commissions

#### **Benefits:**
- **Commission Rate**: 25% on all approved projects
- **Payment Schedule**: Real-time (instant payouts available)
- **Access Level**: Executive-level training and mentorship
- **Support**: 24/7 dedicated support team
- **Marketing Materials**: Full marketing support and joint campaigns
- **Bonus Opportunities**: Uncapped bonus potential and equity participation
- **Strategic Collaboration**: Joint venture opportunities and exclusive territories

#### **Additional Perks:**
- Board advisory position opportunities
- Revenue sharing on referred partner network
- International expansion partnerships
- Custom service development collaboration

## Tier Advancement

### **Automatic Progression:**
- Tiers are reviewed monthly
- Advancement is automatic upon meeting criteria
- No application process required
- Benefits activate immediately upon tier change

### **Tier Maintenance:**
- **Bronze**: No specific requirements after initial qualification
- **Silver**: Maintain 3+ referrals per year
- **Gold**: Maintain 6+ referrals per year
- **Platinum**: Maintain 12+ referrals per year

### **Performance Metrics:**
- Number of successful referrals
- Total commission earned
- Client satisfaction scores
- Referral quality ratings
- Long-term client retention

## Special Recognition Programs

### **Partner of the Month:**
- Recognition on website and social media
- £500 bonus award
- Featured case study
- Speaking opportunity at partner events

### **Annual Excellence Awards:**
- **Top Performer**: Highest total commissions
- **Quality Leader**: Best referral conversion rates
- **Innovation Award**: Creative partnership approaches
- **Community Champion**: Outstanding peer support

**Want to advance your tier?** Focus on quality referrals and client success - the numbers will follow naturally.`,lastUpdated:"2024-01-12",views:1123,helpful:95,tags:["tiers","benefits","advancement","recognition"]}]},{id:"commission-payments",title:"Commission & Payments",description:"Complete information about earnings, payment schedules, and financial aspects",icon:Ue,color:"orange",articles:[{id:"commission-structure-detailed",title:"Detailed Commission Structure",summary:"Comprehensive breakdown of how commissions are calculated and paid",content:`# Detailed Commission Structure

## Base Commission Rates

### **Service-Based Commission Structure:**

#### **Digital Marketing Services:**
- **SEO Services**: 20% commission
- **PPC Management**: 18% commission
- **Social Media Marketing**: 15% commission
- **Content Marketing**: 17% commission

#### **Development Services:**
- **Web Development**: 15% commission
- **Mobile App Development**: 18% commission
- **E-commerce Solutions**: 20% commission
- **Custom Software**: 22% commission

#### **Consulting Services:**
- **Digital Strategy**: 25% commission
- **Business Consulting**: 20% commission
- **Technology Consulting**: 22% commission
- **Growth Consulting**: 25% commission

#### **Enterprise Solutions:**
- **Enterprise Packages**: 12% commission
- **Long-term Contracts**: 15% commission + 5% annual bonus
- **Multi-service Bundles**: 18% commission

### **Tier-Based Multipliers:**
- **Bronze Partner**: Base rates
- **Silver Partner**: Base rates + 3%
- **Gold Partner**: Base rates + 7%
- **Platinum Partner**: Base rates + 10%

## Calculation Examples

### **Example 1: Web Development Project**
- **Project Value**: £15,000
- **Base Commission**: 15% = £2,250
- **Partner Tier**: Silver (+3%) = £2,250 × 1.03 = £2,317.50
- **Final Commission**: £2,317.50

### **Example 2: Enterprise SEO Package**
- **Project Value**: £50,000
- **Base Commission**: 20% = £10,000
- **Partner Tier**: Gold (+7%) = £10,000 × 1.07 = £10,700
- **Quarterly Bonus**: 5% = £535
- **Final Commission**: £11,235

## Bonus Structures

### **Volume Bonuses:**
- **5+ referrals/quarter**: Additional 2% on all commissions
- **10+ referrals/quarter**: Additional 5% on all commissions
- **20+ referrals/quarter**: Additional 10% on all commissions

### **Quality Bonuses:**
- **90%+ approval rate**: £500 quarterly bonus
- **95%+ client satisfaction**: £1,000 quarterly bonus
- **Zero complaints**: £250 monthly bonus

### **Retention Bonuses:**
- **6-month client retention**: 5% additional commission
- **12-month client retention**: 10% additional commission
- **24-month client retention**: 15% additional commission

## Special Commission Opportunities

### **Strategic Client Referrals:**
- **Fortune 500 Companies**: 30% commission rate
- **Government Contracts**: 25% commission rate
- **International Expansion**: 35% commission rate

### **Service Line Development:**
- **New Service Introduction**: 40% commission for first 3 months
- **Beta Testing Participation**: 50% commission during testing period
- **Feedback and Improvement**: £100-£500 per valid suggestion

### **Recurring Revenue Sharing:**
- **Monthly Retainers**: 10% of monthly fees for 12 months
- **Maintenance Contracts**: 15% of annual contract value
- **Subscription Services**: 20% of first year, 10% ongoing

## Commission Tracking

### **Real-Time Dashboard:**
- Live commission tracking
- Project status updates
- Payment history
- Performance analytics

### **Monthly Statements:**
- Detailed commission breakdown
- Tax documentation
- YTD summary
- Projected earnings

### **Annual Reporting:**
- Comprehensive tax forms
- Performance review
- Tier advancement summary
- Growth opportunities

**Questions about commissions?** Our finance team provides detailed explanations and calculations for any project.`,lastUpdated:"2024-01-15",views:1834,helpful:97,tags:["commission","rates","calculation","bonuses"]}]}];function hs({onResultClick:l,className:c}){const[n,r]=u.useState(""),[o,m]=u.useState([]),[b,N]=u.useState(!1),[f,v]=u.useState(!1),[S,p]=u.useState([]),[j,U]=u.useState([]),[D,E]=u.useState("relevance"),[z,B]=u.useState(!1),I=u.useRef(null),i=["How to submit referrals","Commission rates","Payment schedule","Partnership requirements","Training materials","API documentation","Marketing templates","Support contact"],t=[{text:"getting started",category:"Quick Start"},{text:"commission calculation",category:"Payments"},{text:"technical support",category:"Support"},{text:"best practices",category:"Training"},{text:"partner portal",category:"Platform"},{text:"referral tracking",category:"Management"}],a=[...ve.map(s=>({id:s.id,title:s.title,content:s.description,category:s.category,type:"featured",relevanceScore:0,lastUpdated:s.publishedDate||"2024-01-15",views:Math.floor(Math.random()*2e3)+500,helpful:Math.floor(Math.random()*100)+80,tags:s.tags,url:s.link})),...we.flatMap(s=>s.articles.map(d=>({id:d.id,title:d.title,content:d.content,category:s.title,type:"article",relevanceScore:0,lastUpdated:d.lastUpdated,views:d.views,helpful:d.helpful,tags:d.tags,url:`/support/article/${d.id}`}))),...je.map(s=>({id:s.id,title:s.title,content:s.description,category:s.category,type:"resource",relevanceScore:0,lastUpdated:s.lastUpdated||"2024-01-15",views:s.downloads,helpful:Math.floor((s.rating||4.5)*20),tags:[s.category.toLowerCase()],url:s.downloadUrl})),{id:"faq-1",title:"What happens after I submit a referral?",content:"After submitting a referral, our team reviews it within 24 hours. We then contact the client within 48 hours for initial discovery. You receive real-time updates through your partner dashboard and email notifications.",category:"Referrals",type:"faq",relevanceScore:0,lastUpdated:"2024-01-15",views:856,helpful:92,tags:["referrals","process","timeline"],url:"/support/faq/referral-process"},{id:"faq-2",title:"How do I increase my partnership tier?",content:"Partnership tiers are based on successful referrals and total commission earned. Bronze (0-5 referrals), Silver (6-15 referrals), Gold (16-30 referrals), Platinum (31+ referrals). Focus on quality referrals and client success.",category:"Partnership Tiers",type:"faq",relevanceScore:0,lastUpdated:"2024-01-14",views:1234,helpful:95,tags:["tiers","advancement","benefits"],url:"/support/faq/tier-advancement"},{id:"faq-3",title:"Can I refer international clients?",content:"Yes! SISO works with clients globally. We have experience in UK, EU, US, and Asia-Pacific markets. Commission rates may vary by region due to local regulations and service delivery costs.",category:"International",type:"faq",relevanceScore:0,lastUpdated:"2024-01-13",views:445,helpful:87,tags:["international","global","regions"],url:"/support/faq/international-referrals"},{id:"faq-4",title:"What if a client is not satisfied?",content:"Client satisfaction is our top priority. We have a comprehensive project management process, regular check-ins, and revision policies. If issues arise, we work together to resolve them and protect your relationship.",category:"Client Relations",type:"faq",relevanceScore:0,lastUpdated:"2024-01-12",views:667,helpful:89,tags:["satisfaction","quality","relationships"],url:"/support/faq/client-satisfaction"}],w=s=>{if(!s.trim()){m([]);return}N(!0),setTimeout(()=>{const d=s.toLowerCase(),L=d.split(" ").filter(x=>x.length>2);let q=a.map(x=>{let M=0;return x.title.toLowerCase().includes(d)&&(M+=100),L.forEach(K=>{x.title.toLowerCase().includes(K)&&(M+=50)}),x.content.toLowerCase().includes(d)&&(M+=30),L.forEach(K=>{x.content.toLowerCase().includes(K)&&(M+=15)}),x.category.toLowerCase().includes(d)&&(M+=25),x.tags&&x.tags.forEach(K=>{K.toLowerCase().includes(d)&&(M+=20)}),x.views&&x.views>1e3&&(M+=10),x.helpful&&x.helpful>90&&(M+=5),P(C({},x),{relevanceScore:M})});S.length>0&&(q=q.filter(x=>S.includes(x.category))),j.length>0&&(q=q.filter(x=>j.includes(x.type))),q=q.filter(x=>x.relevanceScore>0).sort((x,M)=>{switch(D){case"date":return new Date(M.lastUpdated).getTime()-new Date(x.lastUpdated).getTime();case"popularity":return(M.views||0)-(x.views||0);case"helpful":return(M.helpful||0)-(x.helpful||0);default:return M.relevanceScore-x.relevanceScore}}).slice(0,20),m(q),N(!1)},300)};u.useEffect(()=>{n.length>2?w(n):m([])},[n,S,j,D]);const y=s=>{var d;r(s),B(!1),(d=I.current)==null||d.focus()},k=s=>{p(d=>d.includes(s)?d.filter(L=>L!==s):[...d,s])},W=s=>{U(d=>d.includes(s)?d.filter(L=>L!==s):[...d,s])},G=()=>{p([]),U([]),E("relevance")},V=s=>{switch(s){case"featured":return e.jsx(Je,{className:"h-4 w-4 text-yellow-500"});case"article":return e.jsx(J,{className:"h-4 w-4 text-blue-500"});case"resource":return e.jsx(_e,{className:"h-4 w-4 text-green-500"});case"faq":return e.jsx(se,{className:"h-4 w-4 text-purple-500"});default:return e.jsx(J,{className:"h-4 w-4 text-gray-500"})}};return e.jsxs("div",{className:A("space-y-4",c),children:[e.jsxs("div",{className:"relative",children:[e.jsxs("div",{className:"relative",children:[e.jsx($,{className:"absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400"}),e.jsx(Q,{ref:I,value:n,onChange:s=>r(s.target.value),onFocus:()=>B(!0),placeholder:"Search knowledge base...",className:"pl-10 pr-12 bg-gray-800 border-gray-600 text-white"}),n&&e.jsx(h,{variant:"ghost",size:"sm",onClick:()=>r(""),className:"absolute right-1 top-1/2 transform -translate-y-1/2 h-8 w-8 p-0 text-gray-400 hover:text-white",children:e.jsx(Y,{className:"h-4 w-4"})})]}),e.jsx(X,{children:z&&!n&&e.jsx(g.div,{initial:{opacity:0,y:-10},animate:{opacity:1,y:0},exit:{opacity:0,y:-10},className:"absolute top-full left-0 right-0 mt-2 bg-gray-800 border border-gray-600 rounded-lg shadow-xl z-50",children:e.jsxs("div",{className:"p-4",children:[e.jsx("h4",{className:"text-white font-medium mb-3",children:"Popular Searches"}),e.jsx("div",{className:"grid grid-cols-2 gap-2",children:i.slice(0,6).map((s,d)=>e.jsx("button",{onClick:()=>y(s),className:"text-left text-sm text-gray-300 hover:text-orange-400 transition-colors p-2 rounded hover:bg-gray-700",children:s},d))}),e.jsx("h4",{className:"text-white font-medium mb-3 mt-4",children:"Quick Suggestions"}),e.jsx("div",{className:"flex flex-wrap gap-2",children:t.map((s,d)=>e.jsx(R,{variant:"outline",className:"cursor-pointer hover:bg-orange-500/20 hover:border-orange-500",onClick:()=>y(s.text),children:s.text},d))})]})})})]}),e.jsxs("div",{className:"flex items-center gap-4 flex-wrap",children:[e.jsxs(h,{variant:"outline",size:"sm",onClick:()=>v(!f),className:"border-gray-600 text-gray-300",children:[e.jsx(Ke,{className:"h-4 w-4 mr-2"}),"Filters",(S.length>0||j.length>0)&&e.jsx(R,{className:"ml-2 bg-orange-500 text-white",children:S.length+j.length})]}),e.jsxs(xe,{value:D,onValueChange:E,children:[e.jsx(fe,{className:"w-40 bg-gray-800 border-gray-600 text-white",children:e.jsx(ye,{})}),e.jsxs(be,{children:[e.jsx(O,{value:"relevance",children:"Most Relevant"}),e.jsx(O,{value:"date",children:"Most Recent"}),e.jsx(O,{value:"popularity",children:"Most Popular"}),e.jsx(O,{value:"helpful",children:"Most Helpful"})]})]}),(S.length>0||j.length>0)&&e.jsx(h,{variant:"ghost",size:"sm",onClick:G,className:"text-orange-400 hover:text-orange-300",children:"Clear Filters"})]}),e.jsx(X,{children:f&&e.jsx(g.div,{initial:{opacity:0,height:0},animate:{opacity:1,height:"auto"},exit:{opacity:0,height:0},className:"overflow-hidden",children:e.jsx(F,{className:"bg-gray-800 border-gray-600",children:e.jsx(H,{className:"p-4",children:e.jsxs("div",{className:"grid grid-cols-1 md:grid-cols-2 gap-6",children:[e.jsxs("div",{children:[e.jsx("h4",{className:"text-white font-medium mb-3",children:"Categories"}),e.jsx("div",{className:"space-y-2",children:[...new Set(a.map(s=>s.category))].map(s=>e.jsxs("div",{className:"flex items-center space-x-2",children:[e.jsx(Z,{id:s,checked:S.includes(s),onCheckedChange:()=>k(s)}),e.jsx(T,{htmlFor:s,className:"text-gray-300 text-sm",children:s})]},s))})]}),e.jsxs("div",{children:[e.jsx("h4",{className:"text-white font-medium mb-3",children:"Content Types"}),e.jsx("div",{className:"space-y-2",children:["featured","article","resource","faq"].map(s=>e.jsxs("div",{className:"flex items-center space-x-2",children:[e.jsx(Z,{id:s,checked:j.includes(s),onCheckedChange:()=>W(s)}),e.jsx(T,{htmlFor:s,className:"text-gray-300 text-sm capitalize",children:s==="faq"?"FAQ":s})]},s))})]})]})})})})}),e.jsxs("div",{className:"space-y-4",children:[b&&e.jsx("div",{className:"flex items-center justify-center py-8",children:e.jsxs("div",{className:"flex items-center space-x-2",children:[e.jsx(ee,{className:"h-5 w-5 text-orange-400 animate-pulse"}),e.jsx("span",{className:"text-gray-300",children:"Searching knowledge base..."})]})}),n&&!b&&o.length===0&&e.jsxs("div",{className:"text-center py-8",children:[e.jsxs("div",{className:"text-gray-400 mb-4",children:['No results found for "',n,'"']}),e.jsxs("div",{className:"space-y-2",children:[e.jsx("p",{className:"text-sm text-gray-500",children:"Try:"}),e.jsx("div",{className:"flex flex-wrap gap-2 justify-center",children:i.slice(0,4).map((s,d)=>e.jsx(R,{variant:"outline",className:"cursor-pointer hover:bg-orange-500/20",onClick:()=>y(s),children:s},d))})]})]}),o.length>0&&e.jsxs(e.Fragment,{children:[e.jsxs("div",{className:"text-sm text-gray-400",children:["Found ",o.length," result",o.length!==1?"s":"",' for "',n,'"']}),e.jsx("div",{className:"space-y-3",children:o.map((s,d)=>e.jsx(g.div,{initial:{opacity:0,y:10},animate:{opacity:1,y:0},transition:{duration:.2,delay:d*.05},children:e.jsx(F,{className:"bg-gray-800 border-gray-600 hover:border-orange-500/40 transition-all cursor-pointer group",onClick:()=>l==null?void 0:l(s),children:e.jsx(H,{className:"p-4",children:e.jsxs("div",{className:"flex items-start justify-between",children:[e.jsxs("div",{className:"flex-1",children:[e.jsxs("div",{className:"flex items-center space-x-2 mb-2",children:[V(s.type),e.jsx(R,{variant:"outline",className:"text-xs",children:s.category}),s.type==="featured"&&e.jsx(R,{className:"bg-yellow-500 text-black text-xs",children:"Featured"})]}),e.jsx("h3",{className:"text-white font-medium group-hover:text-orange-400 transition-colors mb-2",children:s.title}),e.jsxs("p",{className:"text-gray-300 text-sm line-clamp-2 mb-3",children:[s.content.substring(0,150),"..."]}),e.jsxs("div",{className:"flex items-center space-x-4 text-xs text-gray-400",children:[e.jsxs("div",{className:"flex items-center space-x-1",children:[e.jsx($e,{className:"h-3 w-3"}),e.jsx("span",{children:new Date(s.lastUpdated).toLocaleDateString()})]}),s.views&&e.jsxs("div",{className:"flex items-center space-x-1",children:[e.jsx(Ye,{className:"h-3 w-3"}),e.jsxs("span",{children:[s.views.toLocaleString()," views"]})]}),s.helpful&&e.jsxs("div",{className:"flex items-center space-x-1",children:[e.jsx(pe,{className:"h-3 w-3"}),e.jsxs("span",{children:[s.helpful,"% helpful"]})]})]}),s.tags&&s.tags.length>0&&e.jsx("div",{className:"flex flex-wrap gap-1 mt-2",children:s.tags.slice(0,3).map((L,q)=>e.jsx(R,{variant:"secondary",className:"text-xs",children:L},q))})]}),e.jsx(_,{className:"h-4 w-4 text-gray-400 group-hover:text-orange-400 transition-colors ml-4"})]})})})},s.id))})]})]})]})}function gs({isOpen:l,onClose:c,initialQuery:n="",className:r}){const o=m=>{console.log("Opening result:",m),m.url&&(m.url.startsWith("http")?window.open(m.url,"_blank"):window.location.href=m.url),c()};return l?e.jsx(X,{children:e.jsx(g.div,{initial:{opacity:0},animate:{opacity:1},exit:{opacity:0},className:"fixed inset-0 bg-black/90 backdrop-blur-sm z-50 flex items-center justify-center p-4",onClick:m=>m.target===m.currentTarget&&c(),children:e.jsxs(g.div,{initial:{scale:.9,opacity:0},animate:{scale:1,opacity:1},exit:{scale:.9,opacity:0},className:A("w-full max-w-6xl max-h-[90vh] bg-black border border-orange-500/20 rounded-xl overflow-hidden",r),children:[e.jsx("div",{className:"border-b border-orange-500/20 p-6",children:e.jsxs("div",{className:"flex items-center justify-between",children:[e.jsxs("div",{className:"flex items-center space-x-3",children:[e.jsx("div",{className:"w-10 h-10 bg-orange-500/20 rounded-lg flex items-center justify-center",children:e.jsx($,{className:"h-5 w-5 text-orange-400"})}),e.jsxs("div",{children:[e.jsx("h2",{className:"text-xl font-semibold text-white",children:"Advanced Search"}),e.jsx("p",{className:"text-gray-400 text-sm",children:"Search through our comprehensive knowledge base"})]})]}),e.jsx(h,{variant:"ghost",size:"sm",onClick:c,className:"text-gray-400 hover:text-white",children:e.jsx(Y,{className:"h-5 w-5"})})]})}),e.jsx("div",{className:"p-6 overflow-y-auto max-h-[calc(90vh-120px)]",children:e.jsx(hs,{onResultClick:o,className:"space-y-6"})})]})})}):null}function Ts(){const[l,c]=u.useState(!1),[n,r]=u.useState(!1),[o,m]=u.useState(!1),b=f=>{console.log("Searching partnership knowledge base for:",f),m(!0)},N=f=>{console.log("Support ticket submitted:",f)};return e.jsxs(e.Fragment,{children:[e.jsx(Ze,{children:e.jsxs("div",{className:"space-y-12",children:[e.jsx(es,{pageTitle:"Partnership Support Center",pageSubtitle:"Get help, find resources, and connect with our team",showDate:!0,pageContext:{pageType:"support",keyMetrics:{primary:{value:"<2 min",label:"Response Time",trend:"Fast"},secondary:{value:"98%",label:"Satisfaction"}}}}),e.jsx(ps,{onSearchClick:()=>m(!0),onAIAssistantClick:()=>c(!0)}),e.jsx(cs,{title:"Partnership Support & Resources",subtitle:"Everything you need to succeed as a SISO partner - help articles, training materials, and direct support 🚀",searchPlaceholder:"Search partnership support articles, guides, and FAQs...",featuredArticles:ve,quickHelpCards:us,helpCenterCards:je,helpCategories:we,backgroundImage:"/images/partnership-support-bg.jpg",onSearch:b,defaultTab:"getting-started",className:"space-y-8"})]})}),e.jsx(ds,{isOpen:l,onToggle:()=>c(!l)}),e.jsx(ms,{isOpen:n,onClose:()=>r(!1),onSubmit:N}),e.jsx(gs,{isOpen:o,onClose:()=>m(!1)}),!l&&!n&&!o&&e.jsx("div",{className:"fixed bottom-6 left-6 z-40",children:e.jsx(h,{onClick:()=>r(!0),className:"h-14 w-14 rounded-full bg-orange-600 hover:bg-orange-700 shadow-lg",title:"Get Support",children:e.jsx(Xe,{className:"h-6 w-6 text-white"})})})]})}export{Ts as default};
