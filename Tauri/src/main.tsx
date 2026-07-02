import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./App.css"; //

// Handle GitHub Pages routing for PWA
(function() {
  const l = window.location;
  const params = new URLSearchParams(l.search);
  const pathFromQuery = params.get('p');
  
  // Если был редирект из 404.html через ?p параметр, удаляем его из URL
  if (pathFromQuery) {
    l.replace(l.protocol + '//' + l.host + '/FindEndPortal/' + (pathFromQuery === '/' ? '' : pathFromQuery));
  }
})();

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
