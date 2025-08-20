import{bI as n,j as e,cA as l,aS as c,cD as d}from"./vendor-C50ijZWh.js";import{F as m,d as s,C as u,a as p,b as x,c as f}from"./index-Blbobipf.js";import{P as h}from"./ProjectCardNavigation-DebhLCYH.js";import{U as g}from"./UserFlowNavigation-BGSOYiRV.js";import{T as j,a as b,b as o,c as i}from"./tabs-CsM4ZGNr.js";import{S as w,a as v,b as y,c as C,d as a}from"./select-Ba1tjTaP.js";import"./libs-B3eAAgHd.js";import"./supabase-D8k0GRjn.js";import"./dialog-CB9qAGL5.js";import"./textarea-B56zo4Tx.js";function W(){const{projectId:r="123"}=n(),t={name:"UbahCrypt Project",description:"A revolutionary blockchain-based cryptocurrency platform with enhanced security features and cross-chain capabilities.",status:"ACTIVE",created_at:"2025-04-01T10:00:00Z"};return e.jsxs(e.Fragment,{children:[e.jsx(m,{name:t.name,description:t.description,status:t.status,created_at:t.created_at}),e.jsx(h,{projectId:r}),e.jsx(g,{projectId:r,projectName:"Agency Onboarding App",status:"draft"}),e.jsxs("div",{className:"container mx-auto py-6",children:[e.jsxs("div",{className:"flex justify-between items-center mb-6",children:[e.jsxs("div",{children:[e.jsx("h2",{className:"text-xl font-bold",children:"Code Export"}),e.jsx("p",{className:"text-sm text-gray-400",children:"Generate boilerplate code from your user flow"})]}),e.jsxs("div",{className:"flex items-center gap-3",children:[e.jsxs(w,{defaultValue:"react",children:[e.jsx(v,{className:"w-[180px]",children:e.jsx(y,{placeholder:"Select Language"})}),e.jsxs(C,{children:[e.jsx(a,{value:"react",children:"React"}),e.jsx(a,{value:"swift",children:"Swift"}),e.jsx(a,{value:"kotlin",children:"Kotlin"}),e.jsx(a,{value:"flutter",children:"Flutter"})]})]}),e.jsxs(s,{children:[e.jsx(l,{className:"mr-2 h-4 w-4"}),"Export Code"]})]})]}),e.jsxs(u,{className:"bg-black/20 border border-siso-text/10",children:[e.jsx(p,{children:e.jsxs("div",{className:"flex justify-between items-center",children:[e.jsxs(x,{className:"text-lg font-medium flex items-center",children:[e.jsx(c,{className:"mr-2 h-5 w-5 text-blue-400"}),"Generated Code"]}),e.jsxs(s,{variant:"outline",size:"sm",className:"h-8",children:[e.jsx(d,{className:"mr-2 h-4 w-4"}),"Copy All"]})]})}),e.jsx(f,{children:e.jsxs(j,{defaultValue:"react",className:"w-full",children:[e.jsxs(b,{className:"mb-4",children:[e.jsx(o,{value:"react",children:"React Router"}),e.jsx(o,{value:"swift",children:"Swift UI"})]}),e.jsx(i,{value:"react",children:e.jsx("div",{className:"bg-gray-900 rounded-md p-4 overflow-x-auto",children:e.jsx("pre",{className:"text-sm text-gray-300 font-mono",children:`import React from 'react';
import { Routes, Route } from 'react-router-dom';
import LoginScreen from './screens/LoginScreen';
import Dashboard from './screens/Dashboard';
import UserProfile from './screens/UserProfile';
import WalletView from './screens/WalletView';
import TradingInterface from './screens/TradingInterface';
import SecurityCenter from './screens/SecurityCenter';

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<LoginScreen />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/profile" element={<UserProfile />} />
      <Route path="/wallet" element={<WalletView />} />
      <Route path="/trading" element={<TradingInterface />} />
      <Route path="/security" element={<SecurityCenter />} />
    </Routes>
  );
}`})})}),e.jsx(i,{value:"swift",children:e.jsx("div",{className:"bg-gray-900 rounded-md p-4 overflow-x-auto",children:e.jsx("pre",{className:"text-sm text-gray-300 font-mono",children:`import SwiftUI

@main
struct UbahCryptApp: App {
    var body: some Scene {
        WindowGroup {
            NavigationView {
                LoginScreen()
            }
        }
    }
}

struct LoginScreen: View {
    @State private var username: String = ""
    @State private var password: String = ""
    
    var body: some View {
        VStack {
            // Login form
            TextField("Username", text: $username)
            SecureField("Password", text: $password)
            
            NavigationLink(destination: DashboardScreen()) {
                Text("Log In")
                    .frame(maxWidth: .infinity)
                    .padding()
                    .background(Color.blue)
                    .foregroundColor(.white)
                    .cornerRadius(8)
            }
        }
        .padding()
        .navigationTitle("Login")
    }
}

struct DashboardScreen: View {
    var body: some View {
        TabView {
            WalletView()
                .tabItem {
                    Label("Wallet", systemImage: "wallet.pass")
                }
            
            TradingView()
                .tabItem {
                    Label("Trading", systemImage: "arrow.left.arrow.right")
                }
            
            ProfileView()
                .tabItem {
                    Label("Profile", systemImage: "person")
                }
        }
        .navigationTitle("Dashboard")
    }
}`})})})]})})]})]})]})}export{W as default};
