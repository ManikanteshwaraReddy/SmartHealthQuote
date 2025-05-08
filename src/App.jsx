import "./App.css";
import { BrowserRouter as Router } from "react-router";
import ScrollToTop from "./components/ui/ScrollToTop";
import AppRouter from "@/routes/Router";

function App() {
  return (
    <>
      <Router>
        <ScrollToTop />
        <AppRouter />
      </Router>
    </>
  );
}

export default App;
