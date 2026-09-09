import BootSequence from "./components/BootSequence";
import Nav from "./components/Nav";
import Convert from "./components/Convert";
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
import MagneticButtons from "./components/MagneticButtons";
import EndCredits from "./components/EndCredits";
import Cursor from "./components/Cursor";
import Particles from "./components/Particles";
import ContactForm from "./components/ContactForm";
import Accordion from "./components/Accordion";

function scrollTo(id: string) {
  document.getElementById(id)?.scrollIntoView({ behavior: "smooth", block: "start" });
}

export default function App() {
  if (window.location.pathname === "/convert") {
    return <Convert />;
  }

  return (
    <div>
      <BootSequence />
      <SpineLine />
      <InkOverlay />
      <SaveFile />
      <TiltCards />
      <AnimationSafetyNet />
      <MagneticButtons />
      <Cursor />
      <Particles />
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
      <ContactForm />
      <Accordion />
      <EndCredits />
    </div>
  );
}
