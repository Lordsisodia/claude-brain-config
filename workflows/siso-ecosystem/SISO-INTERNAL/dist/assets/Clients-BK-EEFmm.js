var ne=Object.defineProperty,ie=Object.defineProperties;var le=Object.getOwnPropertyDescriptors;var F=Object.getOwnPropertySymbols;var G=Object.prototype.hasOwnProperty,H=Object.prototype.propertyIsEnumerable;var Y=(r,o,c)=>o in r?ne(r,o,{enumerable:!0,configurable:!0,writable:!0,value:c}):r[o]=c,U=(r,o)=>{for(var c in o||(o={}))G.call(o,c)&&Y(r,c,o[c]);if(F)for(var c of F(o))H.call(o,c)&&Y(r,c,o[c]);return r},B=(r,o)=>ie(r,le(o));var K=(r,o)=>{var c={};for(var d in r)G.call(r,d)&&o.indexOf(d)<0&&(c[d]=r[d]);if(r!=null&&F)for(var d of F(r))o.indexOf(d)<0&&H.call(r,d)&&(c[d]=r[d]);return c};var E=(r,o,c)=>new Promise((d,n)=>{var h=p=>{try{f(c.next(p))}catch(j){n(j)}},i=p=>{try{f(c.throw(p))}catch(j){n(j)}},f=p=>p.done?d(p.value):Promise.resolve(p.value).then(h,i);f((c=c.apply(r,o)).next())});import{r as u,j as e,y as oe,m as T,bx as ce,bD as O,U as W,aY as J,b3 as Q,H as X,fG as Z,bS as $,L as de,I as xe,bN as pe,bs as ue}from"./vendor-C50ijZWh.js";import{u as he,s as L,C as _,a as k,b as C,c as S,d as R}from"./index-Blbobipf.js";import{P as me,D as ge}from"./dashboard-greeting-card-DLEpxwt_.js";import"./tabs-CsM4ZGNr.js";import"./table-DWISvnW8.js";import"./select-Ba1tjTaP.js";import"./libs-B3eAAgHd.js";import"./supabase-D8k0GRjn.js";const ee=[{value:"not_contacted",label:"Not contacted",color:"status-waiting"},{value:"contacted",label:"Contacted",color:"status-qualified"},{value:"waiting_client",label:"Waiting on client",color:"status-waiting"},{value:"feedback_app",label:"Feedback from app",color:"status-converted"},{value:"declined",label:"Declined",color:"status-declined"}],be={Gym:"tag-green",Construction:"tag-orange","Web3 Trading":"tag-purple",Restaurant:"tag-yellow","MMA GYM":"tag-red",App:"tag-blue","Self Defense Course":"tag-red","Car hire":"tag-yellow",Saas:"tag-purple",Agency:"tag-blue","Football player marketplace":"tag-green",Barbershop:"tag-yellow","E-commerce":"tag-orange",Healthcare:"tag-green",Education:"tag-blue",Finance:"tag-purple","Real Estate":"tag-orange",Travel:"tag-blue",Gaming:"tag-red",Music:"tag-purple",Fashion:"tag-yellow","Food & Beverage":"tag-yellow",Technology:"tag-blue",Consulting:"tag-purple",Other:"tag-orange"},fe={"00000000-0000-0000-0000-000000000001":"Nick Merson","00000000-0000-0000-0000-000000000002":"ALJ","00000000-0000-0000-0000-000000000003":"SISO","00000000-0000-0000-0000-000000000004":"IBBY","00000000-0000-0000-0000-000000000005":"Stevie","placeholder-user-id":"New Affiliate"};function P({value:r,onSave:o,type:c="text",options:d,isUrl:n}){const[h,i]=u.useState(!1),[f,p]=u.useState(r),j=u.useRef(null),y=u.useRef(null),D=()=>{o(f),i(!1)},m=()=>{p(r),i(!1)},N=x=>{x.key==="Enter"?D():x.key==="Escape"&&m()};if(u.useEffect(()=>{h&&(j.current?(j.current.focus(),j.current.select()):y.current&&y.current.focus())},[h]),h)return e.jsx("div",{className:"relative",children:c==="select"&&d?e.jsx("select",{ref:y,value:f,onChange:x=>p(x.target.value),onBlur:D,onKeyDown:N,className:"cell-editor",children:d.map(x=>e.jsx("option",{value:x.value,children:x.label},x.value))}):e.jsx("input",{ref:j,type:"text",value:f,onChange:x=>p(x.target.value),onBlur:D,onKeyDown:N,className:"cell-editor"})});if(n&&r)return e.jsx("a",{href:r,target:"_blank",rel:"noopener noreferrer",className:"url-cell",onClick:x=>x.stopPropagation(),children:r});if(c==="select"&&d){const x=d.find(z=>z.value===r);if(x)return e.jsx("span",{className:`status-tag ${x.color||"status-waiting"}`,children:x.label})}return e.jsx("span",{children:r})}function je(){const[r,o]=u.useState([]),[c,d]=u.useState(!0),[n,h]=u.useState(null),[i,f]=u.useState(null),[p,j]=u.useState(null),[y,D]=u.useState({x:0,y:0,visible:!1}),{toast:m}=he(),N=()=>E(this,null,function*(){try{d(!0);const{data:a,error:t}=yield L.from("portfolio_items").select("*").order("created_at",{ascending:!1});if(t)throw t;const s=(a||[]).map(l=>({id:l.id,title:l.title||"",client_name:l.client_name||"",live_url:l.live_url||"",client_source:l.client_source||"",user_id:l.user_id,project_status:l.project_status||"",mvp_build_status:l.mvp_build_status||"",notion_plan_url:l.notion_plan_url||l.notion_url||"",estimated_price:l.estimated_price||"",initial_contact_date:l.initial_contact_date||"",payment_status:l.payment_status||"",plan_confirmation_status:l.plan_confirmation_status||"",created_at:l.created_at,updated_at:l.updated_at||""}));o(s)}catch(a){console.error("Error loading projects:",a),m({title:"Load Failed",description:"Failed to load projects. Please refresh the page.",variant:"destructive"})}finally{d(!1)}});u.useEffect(()=>{N()},[]);const x=(a,t,s)=>E(this,null,function*(){try{const{error:l}=yield L.from("portfolio_items").update({[t]:s}).eq("id",a);if(l)throw l;m({title:"Project Updated",description:`${t} has been updated successfully.`}),o(w=>w.map(v=>v.id===a?B(U({},v),{[t]:s}):v))}catch(l){console.error("Error updating project:",l),m({title:"Update Failed",description:"Failed to update project. Please try again.",variant:"destructive"})}}),z=()=>E(this,null,function*(){try{const a={title:"New Project",client_name:"Other",live_url:"https://example.vercel.app",client_source:"Personal Network",project_status:"not_contacted",user_id:"9d7b7e7d-a152-4f66-9af9-45d5c544faaf",description:"New project description",technologies:["React"],mvp_build_status:"Planning",notion_plan_url:"",estimated_price:"$0",initial_contact_date:new Date().toISOString().split("T")[0],payment_status:"Not Started",plan_confirmation_status:"Pending"},{error:t}=yield L.from("portfolio_items").insert([a]);if(t)throw t;m({title:"Project Added",description:"New project has been added successfully."}),yield N()}catch(a){console.error("Error adding project:",a),m({title:"Add Failed",description:"Failed to add new project. Please try again.",variant:"destructive"})}}),g=(a,t,s)=>{if(i)return;h({rowIndex:a,field:t}),document.querySelectorAll(".selected").forEach(w=>w.classList.remove("selected"));const l=s.target.closest("tr");l&&l.classList.add("selected")},I=(a,t)=>{["title","client_name","live_url","client_source","project_status"].includes(t)&&f({rowIndex:a,field:t})},A=(a,t,s)=>{const l=r[a];l&&x(l.id,t,s),f(null)},q=()=>{if(n){const a=r[n.rowIndex];if(a){const t=a[n.field];j(String(t||"")),m({title:"Copied",description:"Cell content copied to clipboard."})}}M()},ae=()=>{if(n&&p!==null){const a=r[n.rowIndex];a&&x(a.id,n.field,p)}M()},te=()=>{if(q(),n){const a=r[n.rowIndex];a&&x(a.id,n.field,"")}},se=()=>E(this,null,function*(){if(n){const a=r[n.rowIndex];if(a)try{const{error:t}=yield L.from("portfolio_items").delete().eq("id",a.id);if(t)throw t;m({title:"Project Deleted",description:"Project has been deleted successfully."}),yield N()}catch(t){console.error("Error deleting project:",t),m({title:"Delete Failed",description:"Failed to delete project. Please try again.",variant:"destructive"})}}M()}),re=()=>E(this,null,function*(){if(n){const t=r[n.rowIndex];if(t)try{const a=t,{id:s,created_at:l,updated_at:w}=a,v=K(a,["id","created_at","updated_at"]),{error:V}=yield L.from("portfolio_items").insert([B(U({},v),{title:`${v.title} (Copy)`})]);if(V)throw V;m({title:"Project Duplicated",description:"Project has been duplicated successfully."}),yield N()}catch(s){console.error("Error duplicating project:",s),m({title:"Duplicate Failed",description:"Failed to duplicate project. Please try again.",variant:"destructive"})}}M()}),M=()=>{D({x:0,y:0,visible:!1})},b=a=>{a.target.closest(".editable")&&(a.preventDefault(),D({x:a.pageX,y:a.pageY,visible:!0}))};return u.useEffect(()=>{const a=t=>{if(!n||i)return;const s=n.rowIndex,l=["title","client_name","live_url","client_source","user_id","project_status"],w=l.indexOf(n.field);switch(t.key){case"ArrowUp":t.preventDefault(),s>0&&h({rowIndex:s-1,field:n.field});break;case"ArrowDown":t.preventDefault(),s<r.length-1&&h({rowIndex:s+1,field:n.field});break;case"ArrowLeft":t.preventDefault(),w>0&&h({rowIndex:s,field:l[w-1]});break;case"ArrowRight":t.preventDefault(),w<l.length-1&&h({rowIndex:s,field:l[w+1]});break;case"Enter":n&&I(n.rowIndex,n.field);break;case"Delete":if(n&&!i){const v=r[n.rowIndex];v&&x(v.id,n.field,"")}break}};return document.addEventListener("keydown",a),()=>document.removeEventListener("keydown",a)},[n,i,r]),u.useEffect(()=>{const a=()=>M();return document.addEventListener("click",a),()=>document.removeEventListener("click",a)},[]),c?e.jsxs("div",{className:"airtable-container",children:[e.jsx("div",{className:"toolbar",children:e.jsx("button",{className:"loading",children:"Loading..."})}),e.jsx("div",{className:"table-wrapper",children:e.jsx("div",{style:{padding:"40px",textAlign:"center",color:"#666"},children:"Loading projects..."})})]}):e.jsxs(e.Fragment,{children:[e.jsx("style",{children:`
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        .airtable-container {
            background: #111111;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.5);
            overflow: hidden;
            border: 1px solid #222;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            font-size: 13px;
        }

        .toolbar {
            background: #1a1a1a;
            border-bottom: 1px solid #333;
            padding: 12px 16px;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .toolbar button {
            background: #ff6b35;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            font-size: 13px;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 6px;
            font-weight: 500;
            transition: all 0.2s;
        }

        .toolbar button:hover {
            background: #ff5722;
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(255, 107, 53, 0.3);
        }

        .toolbar button:active {
            transform: translateY(0);
        }

                 .table-wrapper {
             overflow: auto;
             max-height: 70vh;
             position: relative;
             background: #0a0a0a;
             scroll-behavior: smooth;
             -webkit-overflow-scrolling: touch;
         }

         /* Custom scrollbar styling */
         .table-wrapper::-webkit-scrollbar {
             width: 12px;
             height: 12px;
         }

         .table-wrapper::-webkit-scrollbar-track {
             background: #1a1a1a;
             border-radius: 6px;
         }

         .table-wrapper::-webkit-scrollbar-thumb {
             background: #ff6b35;
             border-radius: 6px;
             border: 2px solid #1a1a1a;
         }

         .table-wrapper::-webkit-scrollbar-thumb:hover {
             background: #ff5722;
         }

         .table-wrapper::-webkit-scrollbar-corner {
             background: #1a1a1a;
         }

                 table {
             width: 100%;
             border-collapse: collapse;
             table-layout: fixed;
             position: relative;
             min-width: 2000px;
         }

        th {
            background: #1a1a1a;
            border: 1px solid #333;
            padding: 10px 12px;
            text-align: left;
            font-weight: 600;
            position: sticky;
            top: 0;
            z-index: 10;
            user-select: none;
            cursor: pointer;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            color: #fff;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        th:hover {
            background: #222;
        }

        .header-content {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .column-icon {
            margin-right: 6px;
            opacity: 0.8;
            color: #ff6b35;
        }

        .dropdown-arrow {
            opacity: 0;
            transition: opacity 0.2s;
            color: #ff6b35;
        }

        th:hover .dropdown-arrow {
            opacity: 0.8;
        }

        .row-number {
            background: #1a1a1a;
            border: 1px solid #333;
            text-align: center;
            color: #666;
            font-size: 11px;
            width: 40px;
            position: sticky;
            left: 0;
            z-index: 5;
        }

        td.row-number {
            background: #1a1a1a;
            border-right: 2px solid #333;
        }

        td {
            border: 1px solid #222;
            padding: 10px 12px;
            position: relative;
            background: #111;
            cursor: text;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            color: #e0e0e0;
            transition: all 0.2s;
        }

        td:hover {
            box-shadow: inset 0 0 0 2px #ff6b35;
            z-index: 1;
            background: #1a1a1a;
        }

        .cell-tag {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 16px;
            font-size: 11px;
            font-weight: 600;
            margin-right: 4px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .tag-blue { background: #1a3a52; color: #4a9eff; border: 1px solid #2a4a62; }
        .tag-green { background: #1a4a2a; color: #4aff6a; border: 1px solid #2a5a3a; }
        .tag-yellow { background: #4a3a1a; color: #ffda4a; border: 1px solid #5a4a2a; }
        .tag-red { background: #4a1a1a; color: #ff4a4a; border: 1px solid #5a2a2a; }
        .tag-purple { background: #3a1a4a; color: #da4aff; border: 1px solid #4a2a5a; }
        .tag-orange { background: #4a2a1a; color: #ff6b35; border: 1px solid #5a3a2a; }

        .status-tag {
            display: inline-flex;
            align-items: center;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            text-transform: capitalize;
        }

        .status-qualified { background: #1a4a2a; color: #4aff6a; border: 1px solid #2a5a3a; }
        .status-converted { background: #1a3a52; color: #4a9eff; border: 1px solid #2a4a62; }
        .status-waiting { background: rgba(255, 107, 53, 0.2); color: #ff6b35; border: 1px solid #ff6b35; }
        .status-declined { background: #4a1a1a; color: #ff4a4a; border: 1px solid #5a2a2a; }

        tr:hover td {
            background: #1a1a1a;
        }

        tr.selected td {
            background: rgba(255, 107, 53, 0.1);
            border-color: #333;
        }

        .add-row {
            border: 2px dashed #333;
            background: #0a0a0a;
            padding: 12px 16px;
            text-align: left;
            cursor: pointer;
            color: #666;
            width: 100%;
            display: flex;
            align-items: center;
            gap: 8px;
            transition: all 0.2s;
            font-weight: 500;
        }

        .add-row:hover {
            background: #1a1a1a;
            color: #ff6b35;
            border-color: #ff6b35;
        }

        .context-menu {
            position: absolute;
            background: #1a1a1a;
            border: 1px solid #333;
            border-radius: 6px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.5);
            padding: 4px 0;
            z-index: 1000;
            display: none;
        }

        .context-menu.visible {
            display: block;
        }

        .context-menu-item {
            padding: 10px 20px;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 10px;
            color: #e0e0e0;
            transition: all 0.2s;
        }

        .context-menu-item:hover {
            background: #ff6b35;
            color: #fff;
        }

        .cell-editor {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            border: 2px solid #ff6b35;
            background: #1a1a1a;
            padding: 8px 10px;
            font-family: inherit;
            font-size: inherit;
            z-index: 100;
            box-shadow: 0 4px 12px rgba(255, 107, 53, 0.3);
            color: #fff;
            outline: none;
        }

        .url-cell {
            color: #ff6b35;
            text-decoration: none;
        }

        .url-cell:hover {
            text-decoration: underline;
        }

        .table-wrapper::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }

        .table-wrapper::-webkit-scrollbar-track {
            background: #0a0a0a;
        }

        .table-wrapper::-webkit-scrollbar-thumb {
            background: #333;
            border-radius: 5px;
        }

        .table-wrapper::-webkit-scrollbar-thumb:hover {
            background: #ff6b35;
        }

        @keyframes pulse {
            0% { opacity: 0.6; }
            50% { opacity: 1; }
            100% { opacity: 0.6; }
        }

        .loading {
            animation: pulse 1.5s ease-in-out infinite;
        }
      `}),e.jsxs("div",{className:"airtable-container",children:[e.jsxs("div",{className:"toolbar",children:[e.jsxs("button",{onClick:z,children:[e.jsx("span",{children:"+"})," Add Record"]}),e.jsxs("button",{children:[e.jsx("span",{children:"⚡"})," Automations"]}),e.jsxs("button",{children:[e.jsx("span",{children:"🔍"})," Filter"]}),e.jsxs("button",{children:[e.jsx("span",{children:"↕️"})," Sort"]}),e.jsxs("button",{children:[e.jsx("span",{children:"👁️"})," Hide fields"]})]}),e.jsxs("div",{className:"table-wrapper",children:[e.jsxs("table",{id:"airtableSheet",children:[e.jsx("thead",{children:e.jsxs("tr",{children:[e.jsx("th",{className:"row-number",children:"#"}),e.jsx("th",{style:{width:"200px"},children:e.jsxs("div",{className:"header-content",children:[e.jsxs("span",{children:[e.jsx("span",{className:"column-icon",children:"📝"}),"Project Name"]}),e.jsx("span",{className:"dropdown-arrow",children:"▼"})]})}),e.jsx("th",{style:{width:"150px"},children:e.jsxs("div",{className:"header-content",children:[e.jsxs("span",{children:[e.jsx("span",{className:"column-icon",children:"🏢"}),"Company Niche"]}),e.jsx("span",{className:"dropdown-arrow",children:"▼"})]})}),e.jsx("th",{style:{width:"250px"},children:e.jsxs("div",{className:"header-content",children:[e.jsxs("span",{children:[e.jsx("span",{className:"column-icon",children:"🔗"}),"Development URL"]}),e.jsx("span",{className:"dropdown-arrow",children:"▼"})]})}),e.jsx("th",{style:{width:"150px"},children:e.jsxs("div",{className:"header-content",children:[e.jsxs("span",{children:[e.jsx("span",{className:"column-icon",children:"📍"}),"Source"]}),e.jsx("span",{className:"dropdown-arrow",children:"▼"})]})}),e.jsx("th",{style:{width:"120px"},children:e.jsxs("div",{className:"header-content",children:[e.jsxs("span",{children:[e.jsx("span",{className:"column-icon",children:"👤"}),"Affiliate"]}),e.jsx("span",{className:"dropdown-arrow",children:"▼"})]})}),e.jsx("th",{style:{width:"180px"},children:e.jsxs("div",{className:"header-content",children:[e.jsxs("span",{children:[e.jsx("span",{className:"column-icon",children:"📋"}),"Onboarding Step"]}),e.jsx("span",{className:"dropdown-arrow",children:"▼"})]})}),e.jsx("th",{style:{width:"150px"},children:e.jsxs("div",{className:"header-content",children:[e.jsxs("span",{children:[e.jsx("span",{className:"column-icon",children:"🚀"}),"MVP Build Status"]}),e.jsx("span",{className:"dropdown-arrow",children:"▼"})]})}),e.jsx("th",{style:{width:"250px"},children:e.jsxs("div",{className:"header-content",children:[e.jsxs("span",{children:[e.jsx("span",{className:"column-icon",children:"📄"}),"Notion Plan URL"]}),e.jsx("span",{className:"dropdown-arrow",children:"▼"})]})}),e.jsx("th",{style:{width:"120px"},children:e.jsxs("div",{className:"header-content",children:[e.jsxs("span",{children:[e.jsx("span",{className:"column-icon",children:"💰"}),"Estimated Price"]}),e.jsx("span",{className:"dropdown-arrow",children:"▼"})]})}),e.jsx("th",{style:{width:"150px"},children:e.jsxs("div",{className:"header-content",children:[e.jsxs("span",{children:[e.jsx("span",{className:"column-icon",children:"📅"}),"Initial Contact Date"]}),e.jsx("span",{className:"dropdown-arrow",children:"▼"})]})}),e.jsx("th",{style:{width:"140px"},children:e.jsxs("div",{className:"header-content",children:[e.jsxs("span",{children:[e.jsx("span",{className:"column-icon",children:"💳"}),"Payment Status"]}),e.jsx("span",{className:"dropdown-arrow",children:"▼"})]})}),e.jsx("th",{style:{width:"150px"},children:e.jsxs("div",{className:"header-content",children:[e.jsxs("span",{children:[e.jsx("span",{className:"column-icon",children:"✅"}),"Plan Confirmation"]}),e.jsx("span",{className:"dropdown-arrow",children:"▼"})]})})]})}),e.jsx("tbody",{id:"tableBody",children:r.map((a,t)=>e.jsxs("tr",{children:[e.jsx("td",{className:"row-number",children:t+1}),e.jsx("td",{className:"editable",onClick:s=>g(t,"title",s),onDoubleClick:()=>I(t,"title"),onContextMenu:b,children:(i==null?void 0:i.rowIndex)===t&&(i==null?void 0:i.field)==="title"?e.jsx(P,{value:a.title,onSave:s=>A(t,"title",s)}):a.title}),e.jsx("td",{className:"editable",onClick:s=>g(t,"client_name",s),onDoubleClick:()=>I(t,"client_name"),onContextMenu:b,children:(i==null?void 0:i.rowIndex)===t&&(i==null?void 0:i.field)==="client_name"?e.jsx(P,{value:a.client_name||"",onSave:s=>A(t,"client_name",s)}):e.jsx("span",{className:`cell-tag ${be[a.client_name||""]||"tag-orange"}`,children:a.client_name})}),e.jsx("td",{className:"editable",onClick:s=>g(t,"live_url",s),onDoubleClick:()=>I(t,"live_url"),onContextMenu:b,children:(i==null?void 0:i.rowIndex)===t&&(i==null?void 0:i.field)==="live_url"?e.jsx(P,{value:a.live_url||"",onSave:s=>A(t,"live_url",s),type:"url"}):e.jsx(P,{value:a.live_url||"",onSave:()=>{},isUrl:!0})}),e.jsx("td",{className:"editable",onClick:s=>g(t,"client_source",s),onDoubleClick:()=>I(t,"client_source"),onContextMenu:b,children:(i==null?void 0:i.rowIndex)===t&&(i==null?void 0:i.field)==="client_source"?e.jsx(P,{value:a.client_source||"",onSave:s=>A(t,"client_source",s)}):a.client_source}),e.jsx("td",{className:"editable",onClick:s=>g(t,"user_id",s),onContextMenu:b,children:fe[a.user_id]||a.user_id}),e.jsx("td",{className:"editable",onClick:s=>g(t,"project_status",s),onDoubleClick:()=>I(t,"project_status"),onContextMenu:b,children:(i==null?void 0:i.rowIndex)===t&&(i==null?void 0:i.field)==="project_status"?e.jsx(P,{value:a.project_status||"",onSave:s=>A(t,"project_status",s),type:"select",options:ee}):e.jsx(P,{value:a.project_status||"",onSave:()=>{},type:"select",options:ee})}),e.jsx("td",{className:"editable",onClick:s=>g(t,"mvp_build_status",s),onContextMenu:b,children:e.jsx("span",{className:`status-tag ${a.mvp_build_status==="Completed"?"tag-green":a.mvp_build_status==="In Progress"?"tag-blue":"tag-orange"}`,children:a.mvp_build_status||"Not Started"})}),e.jsx("td",{className:"editable",onClick:s=>g(t,"notion_plan_url",s),onContextMenu:b,children:a.notion_plan_url?e.jsx("a",{href:a.notion_plan_url,target:"_blank",rel:"noopener noreferrer",style:{color:"#ff6b35",textDecoration:"none"},children:"📄 Notion Plan"}):e.jsx("span",{style:{color:"#666"},children:"No plan"})}),e.jsx("td",{className:"editable",onClick:s=>g(t,"estimated_price",s),onContextMenu:b,children:e.jsx("span",{style:{color:a.estimated_price&&a.estimated_price!=="£0.00"?"#4aff6a":"#666",fontWeight:"600"},children:a.estimated_price||"—"})}),e.jsx("td",{className:"editable",onClick:s=>g(t,"initial_contact_date",s),onContextMenu:b,children:e.jsx("span",{style:{color:a.initial_contact_date?"#e0e0e0":"#666"},children:a.initial_contact_date||"—"})}),e.jsx("td",{className:"editable",onClick:s=>g(t,"payment_status",s),onContextMenu:b,children:e.jsx("span",{className:`status-tag ${a.payment_status==="Invoiced"?"tag-green":"tag-orange"}`,children:a.payment_status||"Not Invoiced"})}),e.jsx("td",{className:"editable",onClick:s=>g(t,"plan_confirmation_status",s),onContextMenu:b,children:e.jsx("span",{className:`status-tag ${a.plan_confirmation_status==="Confirmed"?"tag-green":a.plan_confirmation_status==="Declined"?"tag-red":"tag-yellow"}`,children:a.plan_confirmation_status||"Pending"})})]},a.id))})]}),e.jsxs("div",{className:"add-row",onClick:z,children:[e.jsx("span",{children:"+"})," Add a record"]})]})]}),y.visible&&e.jsxs("div",{className:"context-menu visible",style:{left:y.x,top:y.y,position:"fixed"},children:[e.jsxs("div",{className:"context-menu-item",onClick:q,children:[e.jsx("span",{children:"📋"})," Copy"]}),e.jsxs("div",{className:"context-menu-item",onClick:te,children:[e.jsx("span",{children:"✂️"})," Cut"]}),e.jsxs("div",{className:"context-menu-item",onClick:ae,children:[e.jsx("span",{children:"📌"})," Paste"]}),e.jsxs("div",{className:"context-menu-item",onClick:se,children:[e.jsx("span",{children:"🗑️"})," Delete Row"]}),e.jsxs("div",{className:"context-menu-item",onClick:re,children:[e.jsx("span",{children:"📑"})," Duplicate Row"]})]})]})}function De(){const r=oe(),o={totalCommission:2450,activeReferrals:3,conversionRate:68,pipelineValue:75650},c=[{name:"Internal Network",icon:Z,clients:12,conversions:8,revenue:12e3,conversionRate:67,trainingPath:"/partner/training/internal-network"},{name:"LinkedIn Outreach",icon:de,clients:18,conversions:5,revenue:8e3,conversionRate:28,trainingPath:"/partner/training/linkedin-outreach"},{name:"Social Media",icon:xe,clients:8,conversions:2,revenue:3e3,conversionRate:25,trainingPath:"/partner/training/social-media"},{name:"Direct Referrals",icon:pe,clients:5,conversions:4,revenue:15e3,conversionRate:80,trainingPath:"/partner/training/direct-referrals"}],d=n=>{r(n)};return e.jsx(me,{children:e.jsxs("div",{className:"space-y-8",children:[e.jsx(ge,{pageTitle:"Client Management Hub",pageSubtitle:"Your partnership revenue engine - track referrals & commissions",showDate:!0,pageContext:{pageType:"clients",keyMetrics:{primary:{value:"12",label:"Active Clients",trend:"+2"},secondary:{value:"89%",label:"Satisfaction Rate"}},urgentItems:3}}),e.jsxs(T.div,{initial:{opacity:0,y:20},animate:{opacity:1,y:0},transition:{duration:.5},className:"grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4",children:[e.jsxs(_,{className:"bg-black border-orange-500/20",children:[e.jsxs(k,{className:"flex flex-row items-center justify-between space-y-0 pb-2",children:[e.jsx(C,{className:"text-sm font-medium text-gray-400",children:"Total Commission"}),e.jsx(ce,{className:"h-4 w-4 text-orange-400"})]}),e.jsxs(S,{children:[e.jsxs("div",{className:"text-2xl font-bold text-white",children:["£",o.totalCommission.toLocaleString()]}),e.jsxs("div",{className:"flex items-center text-sm text-green-400",children:[e.jsx(O,{className:"h-3 w-3 mr-1"}),"+12% this month"]})]})]}),e.jsxs(_,{className:"bg-black border-orange-500/20",children:[e.jsxs(k,{className:"flex flex-row items-center justify-between space-y-0 pb-2",children:[e.jsx(C,{className:"text-sm font-medium text-gray-400",children:"Active Referrals"}),e.jsx(W,{className:"h-4 w-4 text-orange-400"})]}),e.jsxs(S,{children:[e.jsx("div",{className:"text-2xl font-bold text-white",children:o.activeReferrals}),e.jsxs("div",{className:"flex items-center text-sm text-orange-400",children:[e.jsx(J,{className:"h-3 w-3 mr-1"}),"In progress"]})]})]}),e.jsxs(_,{className:"bg-black border-orange-500/20",children:[e.jsxs(k,{className:"flex flex-row items-center justify-between space-y-0 pb-2",children:[e.jsx(C,{className:"text-sm font-medium text-gray-400",children:"Conversion Rate"}),e.jsx(Q,{className:"h-4 w-4 text-orange-400"})]}),e.jsxs(S,{children:[e.jsxs("div",{className:"text-2xl font-bold text-white",children:[o.conversionRate,"%"]}),e.jsxs("div",{className:"flex items-center text-sm text-green-400",children:[e.jsx(O,{className:"h-3 w-3 mr-1"}),"+5% vs last month"]})]})]}),e.jsxs(_,{className:"bg-black border-orange-500/20",children:[e.jsxs(k,{className:"flex flex-row items-center justify-between space-y-0 pb-2",children:[e.jsx(C,{className:"text-sm font-medium text-gray-400",children:"Pipeline Value"}),e.jsx(X,{className:"h-4 w-4 text-orange-400"})]}),e.jsxs(S,{children:[e.jsxs("div",{className:"text-2xl font-bold text-white",children:["£",o.pipelineValue.toLocaleString()]}),e.jsxs("div",{className:"flex items-center text-sm text-green-400",children:[e.jsx(O,{className:"h-3 w-3 mr-1"}),"+18% potential"]})]})]})]}),e.jsx(T.div,{initial:{opacity:0,y:20},animate:{opacity:1,y:0},transition:{duration:.5,delay:.1},children:e.jsxs(_,{className:"bg-black border-orange-500/20",children:[e.jsxs(k,{children:[e.jsxs(C,{className:"text-xl text-white flex items-center",children:[e.jsx(W,{className:"h-6 w-6 mr-2 text-orange-500"}),"Partner Projects Portfolio"]}),e.jsx("p",{className:"text-gray-400 text-sm",children:"Track and manage your partner projects with Airtable-style interface"})]}),e.jsx(S,{className:"p-0",children:e.jsx(je,{})})]})}),e.jsx(T.div,{initial:{opacity:0,y:20},animate:{opacity:1,y:0},transition:{duration:.5,delay:.2},children:e.jsxs(_,{className:"bg-black border-orange-500/20",children:[e.jsxs(k,{className:"flex flex-row items-center justify-between",children:[e.jsxs("div",{children:[e.jsxs(C,{className:"text-xl text-white flex items-center",children:[e.jsx(Z,{className:"h-6 w-6 mr-2 text-orange-500"}),"Partnership Channels"]}),e.jsx("p",{className:"text-gray-400 text-sm",children:"Track performance by channel and access training resources"})]}),e.jsxs(R,{variant:"default",size:"sm",onClick:()=>r("/partner/training"),className:"bg-orange-600 text-white hover:bg-orange-700 border-0",children:[e.jsx($,{className:"h-4 w-4 mr-2"}),"All Training"]})]}),e.jsx(S,{children:e.jsx("div",{className:"grid grid-cols-1 md:grid-cols-2 gap-4",children:c.map((n,h)=>e.jsx("div",{className:"group",children:e.jsxs("div",{className:"flex items-center justify-between p-4 bg-black border border-gray-700 rounded-lg hover:border-orange-500/30 hover:bg-gray-900/50 transition-all duration-200",children:[e.jsxs("div",{className:"flex items-center space-x-4",children:[e.jsx("div",{className:"w-10 h-10 bg-orange-600/20 rounded-lg flex items-center justify-center",children:e.jsx(n.icon,{className:"h-5 w-5 text-orange-400"})}),e.jsxs("div",{children:[e.jsx("h4",{className:"text-white font-medium",children:n.name}),e.jsxs("div",{className:"flex items-center space-x-3 mt-1 text-sm text-gray-400",children:[e.jsxs("span",{children:[n.clients," clients"]}),e.jsxs("span",{children:[n.conversions," conversions"]}),e.jsxs("span",{children:[n.conversionRate,"% rate"]})]})]})]}),e.jsxs("div",{className:"text-right",children:[e.jsxs("div",{className:"text-white font-bold",children:["£",n.revenue.toLocaleString()]}),e.jsxs(R,{variant:"ghost",size:"sm",onClick:()=>d(n.trainingPath),className:"text-xs text-gray-400 hover:text-orange-400 p-1 h-auto",children:[e.jsx($,{className:"h-3 w-3 mr-1"}),"Training"]})]})]})},h))})})]})}),e.jsx(T.div,{initial:{opacity:0,y:20},animate:{opacity:1,y:0},transition:{duration:.5,delay:.3},children:e.jsxs(_,{className:"bg-black border-orange-500/20",children:[e.jsxs(k,{children:[e.jsxs(C,{className:"text-lg text-white flex items-center",children:[e.jsx($,{className:"h-5 w-5 mr-2 text-orange-500"}),"Quick Training Access"]}),e.jsx("p",{className:"text-gray-400 text-sm",children:"Essential SOPs and training materials for effective client acquisition"})]}),e.jsx(S,{children:e.jsxs("div",{className:"grid grid-cols-2 md:grid-cols-4 gap-3",children:[e.jsxs(R,{variant:"outline",size:"sm",onClick:()=>r("/partner/training/prospecting"),className:"bg-gray-900 border-gray-700 text-gray-300 hover:bg-gray-800 hover:border-orange-500/30 hover:text-orange-400",children:[e.jsx(Q,{className:"h-4 w-4 mr-2"}),"Prospecting"]}),e.jsxs(R,{variant:"outline",size:"sm",onClick:()=>r("/partner/training/follow-up"),className:"bg-gray-900 border-gray-700 text-gray-300 hover:bg-gray-800 hover:border-orange-500/30 hover:text-orange-400",children:[e.jsx(J,{className:"h-4 w-4 mr-2"}),"Follow-up"]}),e.jsxs(R,{variant:"outline",size:"sm",onClick:()=>r("/partner/training/closing"),className:"bg-gray-900 border-gray-700 text-gray-300 hover:bg-gray-800 hover:border-orange-500/30 hover:text-orange-400",children:[e.jsx(X,{className:"h-4 w-4 mr-2"}),"Closing"]}),e.jsxs(R,{variant:"outline",size:"sm",onClick:()=>r("/partner/training"),className:"bg-gray-900 border-gray-700 text-gray-300 hover:bg-gray-800 hover:border-orange-500/30 hover:text-orange-400",children:[e.jsx(ue,{className:"h-4 w-4 mr-2"}),"View All"]})]})})]})})]})})}export{De as default};
