import Nav from "./components/Nav";
import Hero from "./components/Hero";
import Marquee from "./components/Marquee";
import Story from "./components/Story";
import Vectors from "./components/Vectors";
import Pipeline from "./components/Pipeline";
import Compare from "./components/Compare";
import Lab from "./components/Lab";

function scrollTo(id: string) {
  document.getElementById(id)?.scrollIntoView({ behavior: "smooth", block: "start" });
}

export default function App() {
  return (
    <div>
      <Nav onLab={() => scrollTo("lab")} />
      <Hero onPrimary={() => scrollTo("lab")} onSecondary={() => scrollTo("pipeline")} />
      <Marquee />
      <Story />
      <Vectors />
      <Pipeline />
      <Compare />
      <Lab />
      <footer className="footer">
        <div className="footer-inner">
          <span>◈ Aphanis — Zero-Trust AI Provenance Firewall · v1.4.3</span>
          <span>
            <a href="https://github.com/sanyamk23/aphanis" target="_blank" rel="noreferrer">GitHub</a>
            {" · "}
            <a href="#lab" onClick={(e) => { e.preventDefault(); scrollTo("lab"); }}>Open Lab</a>
            {" · "}
            <span style={{ color: "var(--muted)" }}>CLI: pip install aphanis · MCP · REST /api/*</span>
          </span>
        </div>
      </footer>
    </div>
  );
}
