import Nav from "./components/Nav";
import SpineLine from "./components/SpineLine";
import InkOverlay from "./components/InkOverlay";
import HeroInk from "./components/HeroInk";
import Marquee from "./components/Marquee";
import Story from "./components/Story";
import Exhibits from "./components/Exhibits";
import Vectors from "./components/Vectors";
import Pipeline from "./components/Pipeline";
import Compare from "./components/Compare";
import Lab from "./components/Lab";
import Trust from "./components/Trust";
import Integrations from "./components/Integrations";
import SaveFile from "./components/SaveFile";
import Flourish from "./components/Flourish";
import TiltCards from "./components/TiltCards";
import AnimationSafetyNet from "./components/AnimationSafetyNet";

function scrollTo(id: string) {
  document.getElementById(id)?.scrollIntoView({ behavior: "smooth", block: "start" });
}

export default function App() {
  return (
    <div>
      <SpineLine />
      <InkOverlay />
      <SaveFile />
      <TiltCards />
      <AnimationSafetyNet />
      <Nav onLab={() => scrollTo("lab")} />
      <HeroInk onPrimary={() => scrollTo("lab")} onSecondary={() => scrollTo("exhibits")} />
      <Marquee />
      <Story />
      <Flourish />
      <Exhibits />
      <Flourish />
      <Vectors />
      <Pipeline />
      <Flourish />
      <Compare />
      <Lab />
      <Flourish />
      <Trust />
      <Integrations />
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
