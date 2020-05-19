import React from "react";
import ReactDOM from "react-dom";

class App extends React.Component{
    render(){
        return(
            <div ClassName="App">
       
        <ul>
          <li>Instagram</li>
          <li>WhatsApp</li>
          <li>Oculus</li>
        </ul>
      </div>

    )}
}

const wrapper = document.getElementById("app");
wrapper ? ReactDOM.render(<App />, wrapper) : null;