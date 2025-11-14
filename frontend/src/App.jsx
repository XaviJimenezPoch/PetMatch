// import { useState } from 'react'
// import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'
import "./App.css";
import Navbar from "./components/Navbar/Navbar";
import Landpage from "./components/Landpage/Landpage";
import FormRol from "./components/Forms/FormRol";
import FormDialog from "./components/Forms/FormDialog";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import ViewLogin from "./components/Login/ViewLogin";

function App() {
  // const [count, setCount] = useState(0)

  return (
    <BrowserRouter>
      <div
        style={{
          width: "100vw",
          height: "100vh",
          overflow: "hidden",
          display: "flex",
          flexDirection: "column",
        }}
      >
        <Navbar />
        <Routes>
          <Route path="/" element={<Landpage />} />
          <Route
            path="/formulari-dialog"
            element={
              <>
                <Landpage />
                <FormDialog />
              </>
            }
          />
           <Route path="/rol" element={<FormRol />} />
           <Route path="/formulari-acces" element={<ViewLogin />} />
           {/* <Route path="*" element={<FormDialog />} /> */}
        </Routes>
      </div>
    </BrowserRouter>
  );
}
export default App;
