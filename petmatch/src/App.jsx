import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Navbar from './components/Navbar/Navbar'

function App() {
  // const [count, setCount] = useState(0)

  return (
    <>
      <Navbar />
      <div className="container mt-5 pt-5">
        <h1>Benvingut a PetMatch</h1>
        <p>La teva plataforma per trobar la mascota perfecta!</p>
      </div>
    </>
  )
}

export default App
