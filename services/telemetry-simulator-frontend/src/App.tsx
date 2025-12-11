import { useState } from 'react'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="App">
      <header className="App-header">
        <h1>F1 Telemetry Simulator</h1>
        <p>Control and manage F1 telemetry simulation</p>
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
      </header>
    </div>
  )
}

export default App
