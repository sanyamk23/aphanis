export default function Companion({ onShort, onFull }: { onShort: () => void; onFull: () => void }) {
  return (
    <div className="companion">
      <div className="companion-avatar">◈</div>
      <div className="companion-body">
        <span className="companion-name">Aphanis · companion</span>
        <p className="companion-line">&ldquo;You found the ink. Want the short story, or the whole trace?&rdquo;</p>
        <div className="companion-choices">
          <button className="companion-choice" onClick={onShort}>Short story</button>
          <button className="companion-choice primary" onClick={onFull}>The whole trace ▸</button>
        </div>
      </div>
    </div>
  );
}
