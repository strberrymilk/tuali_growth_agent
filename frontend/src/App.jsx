import { useState, useEffect, useRef } from "react"

function LiquidBackground() {
  return (
    <div className="liquid-background">
      <style>{`
        .liquid-background {
          position: fixed;
          inset: 0;
          overflow: hidden;
          z-index: 0;
          background: white;
        }
        .liquid-layer {
          position: absolute;
          inset: -25%;
          filter: blur(80px);
          opacity: 0.95;
        }
        .liquid-layer.one {
          background:
            radial-gradient(circle at 18% 28%, rgba(228,0,43,0.58), transparent 32%),
            radial-gradient(circle at 75% 25%, rgba(241,99,33,0.52), transparent 35%),
            radial-gradient(circle at 45% 78%, rgba(255,184,0,0.45), transparent 38%),
            radial-gradient(circle at 20% 82%, rgba(255,80,120,0.42), transparent 34%);
          animation: liquidDrift 8s ease-in-out infinite alternate;
        }
        .liquid-layer.two {
          opacity: 0.7;
          filter: blur(110px);
          mix-blend-mode: multiply;
          background:
            radial-gradient(circle at 70% 72%, rgba(228,0,43,0.30), transparent 34%),
            radial-gradient(circle at 35% 40%, rgba(255,150,0,0.35), transparent 36%),
            radial-gradient(circle at 85% 35%, rgba(255,210,120,0.35), transparent 35%);
          animation: liquidDriftTwo 10s ease-in-out infinite alternate;
        }
        .soft-white-center {
          position: absolute;
          inset: 0;
          background: radial-gradient(circle at center, rgba(255,255,255,0.55), rgba(255,255,255,0.1), transparent 75%);
          pointer-events: none;
        }
        @keyframes liquidDrift {
          0% { transform: translate3d(-15%,-10%,0) scale(1) rotate(0deg); }
          50% { transform: translate3d(15%,10%,0) scale(1.25) rotate(25deg); }
          100% { transform: translate3d(-10%,15%,0) scale(1.1) rotate(-15deg); }
        }
        @keyframes liquidDriftTwo {
          0% { transform: translate3d(12%,8%,0) scale(1.1) rotate(0deg); }
          50% { transform: translate3d(-18%,-10%,0) scale(1.3) rotate(-25deg); }
          100% { transform: translate3d(10%,-12%,0) scale(1.15) rotate(18deg); }
        }
      `}</style>
      <div className="liquid-layer one" />
      <div className="liquid-layer two" />
      <div className="soft-white-center" />
    </div>
  )
}

function GlassCard({ children, style = {}, onClick, onMouseEnter, onMouseLeave }) {
  return (
    <div
      onClick={onClick}
      onMouseEnter={onMouseEnter}
      onMouseLeave={onMouseLeave}
      style={{
        background: "rgba(255,255,255,0.25)",
        backdropFilter: "blur(32px) saturate(180%)",
        WebkitBackdropFilter: "blur(32px) saturate(180%)",
        border: "1px solid rgba(255,255,255,0.6)",
        borderRadius: "24px",
        boxShadow: "0 8px 32px rgba(0,0,0,0.08), inset 0 1.5px 0 rgba(255,255,255,0.85), inset 0 -1px 0 rgba(255,255,255,0.3)",
        ...style
      }}
    >
      {children}
    </div>
  )
}

export default function App() {
  const [screen, setScreen] = useState("inicio")

  const goToProcesando = () => {
    setScreen("procesando")
    setTimeout(() => setScreen("chat"), 4500)
  }

  return (
    <div style={{minHeight: "100vh", fontFamily: "Nunito, sans-serif", position: "relative"}}>
      {screen !== "inicio" && screen !== "bienvenido" && screen !== "herramientas" && <LiquidBackground />}
      <div style={{position: "relative", zIndex: 1}}>
        {screen === "inicio" && <PaginaInicio onAllie={() => setScreen("bienvenido")} />}
        {screen === "bienvenido" && <PantallaBienvenido onNext={() => setScreen("herramientas")} />}
        {screen === "herramientas" && <PantallaHerramientas onNext={goToProcesando} />}
        {screen === "procesando" && <PantallaProcesando />}
        {screen === "chat" && <PantallaChat />}
      </div>
    </div>
  )
}

function PaginaInicio({ onAllie }) {
  return (
    <div style={{minHeight: "100vh", background: "white"}}>
      <div style={{background: "linear-gradient(to right, #E4002B, #F16321)", padding: "0 40px", display: "flex", alignItems: "center", justifyContent: "space-between", height: "64px", position: "sticky", top: 0, zIndex: 100}}>
        <div style={{display: "flex", alignItems: "center", gap: "32px"}}>
          <span style={{color: "white", fontWeight: "900", fontSize: "26px", letterSpacing: "-1px"}}>túali</span>
          <div style={{display: "flex", gap: "4px"}}>
            {["Inicio", "Productos", "Pedidos", "Gana"].map(tab => (
              <button key={tab} style={{background: "transparent", border: "1px solid transparent", borderRadius: "8px", color: "rgba(255,255,255,0.85)", padding: "6px 14px", fontSize: "14px", cursor: "pointer", fontFamily: "Nunito, sans-serif"}}>
                {tab}
              </button>
            ))}
            <button
              onClick={onAllie}
              style={{background: "rgba(255,255,255,0.22)", border: "1px solid rgba(255,255,255,0.55)", borderRadius: "8px", color: "white", padding: "6px 16px", fontSize: "14px", fontWeight: "700", cursor: "pointer", fontFamily: "Nunito, sans-serif", transition: "all 0.2s"}}
              onMouseEnter={e => e.currentTarget.style.background = "rgba(255,255,255,0.38)"}
              onMouseLeave={e => e.currentTarget.style.background = "rgba(255,255,255,0.22)"}
            >
              ✨ Allie
            </button>
          </div>
        </div>
        <div style={{display: "flex", alignItems: "center", gap: "12px"}}>
          <div style={{background: "rgba(255,255,255,0.15)", borderRadius: "20px", padding: "6px 16px", display: "flex", alignItems: "center", gap: "8px", width: "200px"}}>
            <span style={{color: "rgba(255,255,255,0.7)"}}>🔍</span>
            <span style={{color: "rgba(255,255,255,0.6)", fontSize: "14px"}}>Buscar</span>
          </div>
          <div style={{width: "36px", height: "36px", borderRadius: "50%", background: "white", display: "flex", alignItems: "center", justifyContent: "center", fontWeight: "700", color: "#E4002B", fontSize: "12px"}}>AC</div>
        </div>
      </div>

      <div style={{background: "white", padding: "8px 40px", borderBottom: "1px solid #eee", display: "flex", justifyContent: "space-between", alignItems: "center"}}>
        <div>
          <span style={{fontSize: "12px", color: "#999"}}>Punto de venta: </span>
          <span style={{fontSize: "13px", fontWeight: "700"}}>Abarrotes Chabelita</span>
          <span style={{fontSize: "12px", color: "#999"}}> · Mar ártico no.201, mazatlán</span>
        </div>
        <span style={{fontSize: "12px", background: "#e8f5e9", color: "#22C55E", padding: "3px 12px", borderRadius: "10px", fontWeight: "600"}}>● Pedido Confirmado · #39E2C00A</span>
      </div>

      <div style={{maxWidth: "1200px", margin: "0 auto", padding: "28px 40px"}}>
        <div style={{display: "flex", gap: "10px", marginBottom: "24px"}}>
          <div style={{background: "#E4002B", borderRadius: "10px", padding: "10px 24px"}}>
            <span style={{color: "white", fontWeight: "900", fontSize: "18px"}}>Coca-Cola</span>
          </div>
          <div style={{background: "#f5e6c8", borderRadius: "10px", padding: "10px 24px"}}>
            <span style={{color: "#8B6914", fontWeight: "700", fontSize: "18px"}}>Bokados</span>
          </div>
        </div>

        <div style={{display: "grid", gridTemplateColumns: "2fr 1fr", gap: "20px", marginBottom: "24px"}}>
          <div
            onClick={onAllie}
            style={{background: "linear-gradient(135deg, #fff0f0, #fff5ee)", borderRadius: "20px", padding: "36px", border: "2px solid rgba(228,0,43,0.1)", cursor: "pointer", display: "flex", justifyContent: "space-between", alignItems: "center", transition: "all 0.2s ease"}}
            onMouseEnter={e => { e.currentTarget.style.transform = "scale(1.01)"; e.currentTarget.style.boxShadow = "0 16px 50px rgba(228,0,43,0.15)" }}
            onMouseLeave={e => { e.currentTarget.style.transform = "scale(1)"; e.currentTarget.style.boxShadow = "none" }}
          >
            <div>
              <div style={{display: "flex", alignItems: "center", gap: "10px", marginBottom: "10px"}}>
                <span style={{fontSize: "28px"}}>✨</span>
                <span style={{fontWeight: "900", fontSize: "30px", background: "linear-gradient(to right, #E4002B, #F16321)", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent"}}>Allie</span>
              </div>
              <p style={{fontWeight: "700", fontSize: "20px", color: "#1A1A1A", marginBottom: "8px"}}>Tu asistente de crecimiento</p>
              <p style={{fontSize: "14px", color: "#666", marginBottom: "24px", maxWidth: "340px"}}>Recibe recomendaciones personalizadas basadas en tu historial de Tuali para hacer crecer tu negocio.</p>
              <button style={{background: "linear-gradient(to right, #E4002B, #F16321)", border: "none", borderRadius: "12px", padding: "13px 26px", color: "white", fontWeight: "700", cursor: "pointer", fontSize: "14px", fontFamily: "Nunito, sans-serif"}}>
                Comenzar con Allie →
              </button>
            </div>
            <div style={{fontSize: "100px", userSelect: "none"}}>🤖</div>
          </div>

          <div style={{background: "linear-gradient(135deg, #fff8e1, #fff3cd)", borderRadius: "20px", padding: "28px", border: "1px solid rgba(255,184,0,0.2)", display: "flex", flexDirection: "column", justifyContent: "space-between"}}>
            <div>
              <p style={{fontSize: "20px", fontWeight: "900", color: "#E4002B", lineHeight: "1.3", marginBottom: "8px"}}>¡Ya acumulaste Puntos, ahora hazlos valer!</p>
              <p style={{fontSize: "13px", color: "#888", marginBottom: "20px"}}>Canjea por productos Coca-Cola.</p>
            </div>
            <div style={{background: "linear-gradient(to right, #E4002B, #F16321)", borderRadius: "10px", padding: "8px 18px", display: "inline-block", width: "fit-content"}}>
              <span style={{color: "white", fontWeight: "900", fontSize: "18px"}}>gana</span>
            </div>
          </div>
        </div>

        <div style={{background: "white", borderRadius: "16px", padding: "22px 28px", marginBottom: "20px", boxShadow: "0 2px 12px rgba(0,0,0,0.06)"}}>
          <h3 style={{fontWeight: "700", fontSize: "16px", marginBottom: "18px"}}>Categorías</h3>
          <div style={{display: "flex", gap: "20px"}}>
            {[
              {icon: "👑", label: "Tus más vendidos"},
              {icon: "🏷️", label: "Promos", active: true},
              {icon: "🥤", label: "Refrescos"},
              {icon: "💧", label: "Agua"},
              {icon: "🥛", label: "Lácteos"},
              {icon: "🧃", label: "Jugos"},
              {icon: "⚡", label: "Energéticas"},
            ].map(cat => (
              <div key={cat.label} style={{display: "flex", flexDirection: "column", alignItems: "center", gap: "8px", cursor: "pointer"}}>
                <div style={{width: "64px", height: "64px", borderRadius: "14px", border: cat.active ? "2px solid #E4002B" : "1px solid #eee", background: "white", display: "flex", alignItems: "center", justifyContent: "center", fontSize: "28px"}}>
                  {cat.icon}
                </div>
                <span style={{fontSize: "11px", textAlign: "center", fontWeight: cat.active ? "700" : "400", color: cat.active ? "#E4002B" : "#666"}}>{cat.label}</span>
              </div>
            ))}
          </div>
        </div>

        <div style={{background: "white", borderRadius: "16px", padding: "22px 28px", boxShadow: "0 2px 12px rgba(0,0,0,0.06)"}}>
          <div style={{display: "flex", justifyContent: "space-between", alignItems: "center"}}>
            <div style={{display: "flex", alignItems: "center", gap: "12px"}}>
              <span style={{fontSize: "26px"}}>🧺</span>
              <div>
                <p style={{fontWeight: "700", fontSize: "15px"}}>Vuelve a surtir</p>
                <p style={{fontSize: "13px", color: "#999"}}>De pedidos anteriores, listos para reponer.</p>
              </div>
            </div>
            <span style={{color: "#E4002B", fontSize: "13px", fontWeight: "600", cursor: "pointer"}}>Ver todos ›</span>
          </div>
        </div>
      </div>
    </div>
  )
}

function PantallaBienvenido({ onNext }) {
  const [phase, setPhase] = useState("logo")

  useEffect(() => {
    const t = setTimeout(() => setPhase("start"), 1900)
    return () => clearTimeout(t)
  }, [])

  return (
    <div style={{position:"fixed",inset:0,display:"flex",alignItems:"center",justifyContent:"center",zIndex:50,overflow:"hidden",background:"linear-gradient(135deg, #E4002B 0%, #F16321 60%, #FFB800 100%)"}}>
      <style>{`
        @keyframes logoIntro {
          0% { opacity:0; transform:scale(0.82) translateY(24px); filter:blur(8px); }
          100% { opacity:1; transform:scale(1) translateY(0); filter:blur(0); }
        }
        @keyframes logoMoveUp {
          0% { transform:translateY(0) scale(1); opacity:1; }
          100% { transform:translateY(-145px) scale(0.62); opacity:1; }
        }
        @keyframes contentUp {
          0% { opacity:0; transform:translateY(90px); filter:blur(10px); }
          100% { opacity:1; transform:translateY(0); filter:blur(0); }
        }
        @keyframes buttonUp {
          0% { opacity:0; transform:translateY(36px) scale(0.96); }
          100% { opacity:1; transform:translateY(0) scale(1); }
        }
      `}</style>

      <div style={{textAlign:"center",color:"white",width:"100%",padding:"0 32px"}}>
        <h1 style={{
          fontSize:"clamp(76px,13vw,170px)",
          fontWeight:"950",
          letterSpacing:"-8px",
          lineHeight:"0.9",
          margin:0,
          color:"white",
          animation: phase === "logo"
            ? "logoIntro 1s cubic-bezier(0.16,1,0.3,1) forwards"
            : "logoMoveUp 1s cubic-bezier(0.16,1,0.3,1) forwards",
        }}>
          tuali
        </h1>

        {phase === "start" && (
          <div style={{marginTop:"-20px",animation:"contentUp 1s cubic-bezier(0.16,1,0.3,1) forwards"}}>
            <p style={{fontSize:"clamp(24px,3.5vw,44px)",fontWeight:"500",lineHeight:"1.25",maxWidth:"680px",margin:"0 auto 42px",color:"white"}}>
              Empecemos con tu análisis de negocio
            </p>
            <button
              onClick={onNext}
              style={{
                background:"white",color:"#E4002B",border:"none",borderRadius:"999px",
                padding:"16px 46px",fontSize:"18px",fontWeight:"800",
                cursor:"pointer",fontFamily:"Nunito,sans-serif",
                boxShadow:"0 18px 50px rgba(0,0,0,0.2)",
                animation:"buttonUp 0.8s cubic-bezier(0.16,1,0.3,1) 0.15s both",
                transition:"transform 0.2s ease",
              }}
              onMouseEnter={e => e.currentTarget.style.transform="scale(1.05)"}
              onMouseLeave={e => e.currentTarget.style.transform="scale(1)"}
            >
              Continuar →
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

function PantallaHerramientas({ onNext }) {
  const btnBase = {
    width:"100%", padding:"15px 18px", borderRadius:"14px",
    border:"1px solid rgba(255,255,255,0.35)",
    background:"rgba(255,255,255,0.15)",
    backdropFilter:"blur(16px)",
    WebkitBackdropFilter:"blur(16px)",
    color:"white", fontWeight:"600", fontSize:"15px",
    cursor:"pointer", fontFamily:"Nunito,sans-serif", transition:"all 0.2s",
    textAlign:"left", display:"flex", alignItems:"center", justifyContent:"space-between",
    boxShadow:"inset 0 1px 0 rgba(255,255,255,0.4)"
  }

  return (
    <div style={{position:"fixed",inset:0,zIndex:50,overflow:"hidden"}}>
      <style>{`@keyframes fadeInUp{from{opacity:0;transform:translateY(30px)}to{opacity:1;transform:translateY(0)}}`}</style>

      <div style={{position:"absolute",inset:0,background:"linear-gradient(135deg, #E4002B 0%, #F16321 60%, #FFB800 100%)"}}/>

      <div style={{position:"relative",zIndex:1,height:"100%",display:"flex",alignItems:"center",justifyContent:"center"}}>
        <div style={{
          background:"rgba(255,255,255,0.15)",
          backdropFilter:"blur(32px) saturate(180%)",
          WebkitBackdropFilter:"blur(32px) saturate(180%)",
          border:"1px solid rgba(255,255,255,0.4)",
          borderRadius:"24px",
          boxShadow:"0 8px 32px rgba(0,0,0,0.12), inset 0 1.5px 0 rgba(255,255,255,0.7), inset 0 -1px 0 rgba(255,255,255,0.2)",
          padding:"40px",maxWidth:"500px",width:"90%",
          animation:"fadeInUp 0.6s ease forwards"
        }}>
          <div style={{display:"flex",alignItems:"center",gap:"10px",marginBottom:"10px"}}>
            <span style={{fontWeight:"900",fontSize:"20px",color:"white"}}>✨ Allie</span>
          </div>
          <p style={{fontSize:"16px",fontWeight:"700",color:"white",marginBottom:"6px",lineHeight:"1.4"}}>
            Para generar el análisis de tu negocio, utilizo tu información en Tuali.
          </p>
          <p style={{fontSize:"14px",color:"rgba(255,255,255,0.8)",marginBottom:"24px",lineHeight:"1.5"}}>
            ¿Te gustaría complementar el análisis con alguna de estas herramientas de ventas?
          </p>
          <div style={{display:"flex",flexDirection:"column",gap:"10px"}}>
            <button
              onClick={onNext}
              style={{...btnBase,background:"white",color:"#E4002B",border:"none",fontWeight:"700",boxShadow:"0 8px 24px rgba(0,0,0,0.15)"}}
              onMouseEnter={e => e.currentTarget.style.transform="scale(1.02)"}
              onMouseLeave={e => e.currentTarget.style.transform="scale(1)"}
            >
              <span>Continuar solo con Tuali</span><span>→</span>
            </button>
            {["Yomp!","Terminal de pago","Ingresar datos manualmente"].map(opt => (
              <button key={opt} style={btnBase}
                onMouseEnter={e => e.currentTarget.style.background="rgba(255,255,255,0.28)"}
                onMouseLeave={e => e.currentTarget.style.background="rgba(255,255,255,0.15)"}
              >
                <span>{opt}</span><span style={{color:"rgba(255,255,255,0.7)"}}>→</span>
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

function PantallaProcesando() {
  return (
    <div style={{
      position: "fixed",
      inset: 0,
      background: "white",
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      zIndex: 50
    }}>
      <style>{`
        .fluid-orb-wrapper { position:relative; width:300px; height:300px; display:flex; align-items:center; justify-content:center; }
        .fluid-orb-glow { position:absolute; width:360px; height:360px; border-radius:999px; background:radial-gradient(circle,rgba(255,184,0,0.45),rgba(241,99,33,0.25),rgba(228,0,43,0.12),transparent 70%); filter:blur(45px); animation:glowBreath 4s ease-in-out infinite; }
        .fluid-orb { position:relative; width:250px; height:250px; overflow:hidden; border-radius:54% 46% 48% 52% / 48% 55% 45% 52%; background: radial-gradient(circle at 32% 62%,rgba(220,40,130,0.82),transparent 34%), radial-gradient(circle at 48% 48%,rgba(255,75,120,0.74),transparent 40%), radial-gradient(circle at 35% 32%,rgba(255,140,20,0.85),transparent 34%), radial-gradient(circle at 72% 35%,rgba(255,225,120,0.82),transparent 42%), radial-gradient(circle at 75% 72%,rgba(255,240,160,0.72),transparent 44%); filter:blur(0.2px); animation:orbMorph 7s ease-in-out infinite,orbFloat 8s ease-in-out infinite; box-shadow:0 24px 90px rgba(228,0,43,0.18),0 0 110px rgba(255,184,0,0.25); }
        .fluid-orb::before { content:""; position:absolute; inset:-35%; background: radial-gradient(circle at 42% 55%,rgba(255,40,130,0.75),transparent 30%), radial-gradient(circle at 35% 28%,rgba(255,130,20,0.85),transparent 28%), radial-gradient(circle at 76% 32%,rgba(255,230,120,0.80),transparent 42%); filter:blur(22px); animation:innerFlowA 5.5s ease-in-out infinite; mix-blend-mode:screen; }
        .fluid-orb::after { content:""; position:absolute; inset:-30%; background: radial-gradient(circle at 55% 55%,rgba(220,60,150,0.65),transparent 36%), radial-gradient(circle at 75% 38%,rgba(255,220,95,0.74),transparent 44%); filter:blur(26px); animation:innerFlowB 6.8s ease-in-out infinite; mix-blend-mode:multiply; }
        .orb-soft-mask { position:absolute; inset:0; border-radius:inherit; background:radial-gradient(circle at 50% 50%,transparent 30%,rgba(255,255,255,0.18) 100%); pointer-events:none; }

        @keyframes orbMorph {
          0%{border-radius:52% 48% 45% 55%/50% 45% 55% 50%}
          25%{border-radius:58% 42% 54% 46%/42% 58% 45% 55%}
          50%{border-radius:45% 55% 60% 40%/58% 42% 52% 48%}
          75%{border-radius:60% 40% 42% 58%/45% 55% 58% 42%}
          100%{border-radius:52% 48% 45% 55%/50% 45% 55% 50%}
        }

        @keyframes orbFloat {
          0%,100%{transform:translateY(0) scale(1)}
          50%{transform:translateY(-8px) scale(1.03)}
        }

        @keyframes innerFlowA {
          0%{transform:translate(-12%,6%) rotate(0deg) scale(1)}
          50%{transform:translate(12%,-10%) rotate(55deg) scale(1.25)}
          100%{transform:translate(-12%,6%) rotate(0deg) scale(1)}
        }

        @keyframes innerFlowB {
          0%{transform:translate(10%,-6%) rotate(0deg) scale(1.1)}
          50%{transform:translate(-12%,12%) rotate(-70deg) scale(1.35)}
          100%{transform:translate(10%,-6%) rotate(0deg) scale(1.1)}
        }

        @keyframes glowBreath {
          0%,100%{opacity:0.52;transform:scale(0.95)}
          50%{opacity:0.85;transform:scale(1.12)}
        }

        @keyframes fadeInUp {
          from{opacity:0;transform:translateY(18px)}
          to{opacity:1;transform:translateY(0)}
        }
      `}</style>

      <div className="fluid-orb-wrapper">
        <div className="fluid-orb-glow" />
        <div className="fluid-orb">
          <div className="orb-soft-mask" />
        </div>
      </div>

      <div style={{
        textAlign: "center",
        marginTop: "42px",
        animation: "fadeInUp 0.8s ease 0.3s both"
      }}>
        <p style={{
          fontSize: "22px",
          fontWeight: "800",
          color: "#1A1A1A",
          marginBottom: "10px"
        }}>
          Estoy generando tu análisis de negocio
        </p>

        <p style={{
          fontSize: "15px",
          color: "#777"
        }}>
          Esto tomará solo unos segundos
        </p>
      </div>
    </div>
  )
}

function PantallaChat() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState("")
  const [isTyping, setIsTyping] = useState(false)
  const [started, setStarted] = useState(false)
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages, isTyping])

  const handleSend = () => {
    const msg = input.trim()
    if (!msg) return
    setInput("")
    setStarted(true)
    setMessages(prev => [...prev, { from: "user", text: msg }])
    setIsTyping(true)
    setTimeout(() => {
      setIsTyping(false)
      setMessages(prev => [...prev, { from: "allie", text: "Entendido, voy a trabajar en eso para ti." }])
    }, 1800)
  }

  const AllieAvatar = () => (
    <div style={{width:"32px",height:"32px",borderRadius:"50%",background:"linear-gradient(135deg,#E4002B,#F16321,#FFB800)",display:"flex",alignItems:"center",justifyContent:"center",fontSize:"14px",flexShrink:0}}>✨</div>
  )

  return (
    <div style={{position:"fixed",inset:0,display:"flex",flexDirection:"column",zIndex:50,background:"white",overflow:"hidden"}}>
      <style>{`
        @keyframes fadeInUp { from{opacity:0;transform:translateY(12px)} to{opacity:1;transform:translateY(0)} }
        @keyframes typingDot { 0%,80%,100%{transform:scale(0.6);opacity:0.3} 40%{transform:scale(1);opacity:1} }

        @keyframes intenseRibbonOne {
          0% {
            transform: translate3d(-12%, -12%, 0) rotate(-8deg) scaleX(1);
            background-position: 0% 50%;
          }
          50% {
            transform: translate3d(10%, 6%, 0) rotate(-2deg) scaleX(1.16);
            background-position: 100% 50%;
          }
          100% {
            transform: translate3d(-6%, 10%, 0) rotate(-13deg) scaleX(1.05);
            background-position: 0% 50%;
          }
        }

        @keyframes intenseRibbonTwo {
          0% {
            transform: translate3d(10%, 8%, 0) rotate(7deg) scaleX(1.05);
            background-position: 100% 50%;
          }
          50% {
            transform: translate3d(-10%, -8%, 0) rotate(1deg) scaleX(1.24);
            background-position: 0% 50%;
          }
          100% {
            transform: translate3d(6%, -4%, 0) rotate(11deg) scaleX(1.08);
            background-position: 100% 50%;
          }
        }

        @keyframes intenseRibbonThree {
          0% {
            transform: translate3d(-4%, 0%, 0) rotate(-4deg) scaleX(1);
            opacity: 0.9;
          }
          50% {
            transform: translate3d(6%, -5%, 0) rotate(4deg) scaleX(1.18);
            opacity: 1;
          }
          100% {
            transform: translate3d(-8%, 4%, 0) rotate(-7deg) scaleX(1.04);
            opacity: 0.95;
          }
        }

        .chat-msg { animation: fadeInUp 0.3s ease forwards; }
        .typing-dot { width:7px;height:7px;border-radius:50%;background:#ccc;display:inline-block;margin:0 2px;animation:typingDot 1.2s ease-in-out infinite; }
        .typing-dot:nth-child(2){animation-delay:0.2s}
        .typing-dot:nth-child(3){animation-delay:0.4s}
        .send-btn { width:40px;height:40px;border-radius:50%;background:linear-gradient(to right,#E4002B,#F16321);border:none;cursor:pointer;display:flex;align-items:center;justify-content:center;color:white;font-size:18px;flex-shrink:0;transition:transform 0.15s;box-shadow:0 4px 14px rgba(228,0,43,0.25); }
        .send-btn:hover{transform:scale(1.08)}
        .send-btn:disabled{background:#e5e5e5;box-shadow:none;cursor:not-allowed}
      `}</style>

      <div style={{position:"absolute",inset:0,overflow:"hidden",pointerEvents:"none",zIndex:0}}>
        <div style={{
          position:"absolute",
          top:"34%",
          left:"-24%",
          width:"150%",
          height:"36%",
          borderRadius:"999px",
          background:"linear-gradient(90deg, transparent 0%, rgba(228,0,43,0.78) 18%, rgba(255,32,32,0.88) 34%, rgba(241,99,33,0.92) 52%, rgba(255,122,0,0.82) 68%, rgba(255,184,0,0.58) 82%, transparent 100%)",
          backgroundSize:"220% 220%",
          filter:"blur(26px)",
          transformOrigin:"center",
          animation:"intenseRibbonOne 9s ease-in-out infinite alternate",
          opacity:0.95
        }}/>

        <div style={{
          position:"absolute",
          top:"43%",
          left:"-22%",
          width:"145%",
          height:"30%",
          borderRadius:"999px",
          background:"linear-gradient(90deg, transparent 0%, rgba(255,184,0,0.60) 18%, rgba(255,122,0,0.85) 34%, rgba(241,99,33,0.92) 52%, rgba(228,0,43,0.86) 72%, transparent 100%)",
          backgroundSize:"240% 240%",
          filter:"blur(34px)",
          transformOrigin:"center",
          animation:"intenseRibbonTwo 11s ease-in-out infinite alternate",
          mixBlendMode:"multiply",
          opacity:0.85
        }}/>

        <div style={{
          position:"absolute",
          top:"50%",
          left:"-18%",
          width:"136%",
          height:"18%",
          borderRadius:"999px",
          background:"linear-gradient(90deg, transparent 0%, rgba(228,0,43,0.40) 18%, rgba(241,99,33,0.70) 45%, rgba(255,184,0,0.45) 70%, transparent 100%)",
          filter:"blur(42px)",
          transformOrigin:"center",
          animation:"intenseRibbonThree 7s ease-in-out infinite alternate",
          opacity:0.9
        }}/>

        <div style={{
          position:"absolute",
          inset:0,
          background:"linear-gradient(to bottom, rgba(255,255,255,0.02) 0%, rgba(255,255,255,0.22) 32%, rgba(255,255,255,0.80) 62%, white 100%)",
          pointerEvents:"none"
        }}/>
      </div>

      <div style={{padding:"16px 24px",borderBottom:"1px solid rgba(0,0,0,0.06)",display:"flex",alignItems:"center",gap:"10px",position:"relative",zIndex:1,background:"rgba(255,255,255,0.7)",backdropFilter:"blur(16px)",WebkitBackdropFilter:"blur(16px)"}}>
        <div style={{width:"36px",height:"36px",borderRadius:"50%",background:"linear-gradient(135deg,#E4002B,#F16321,#FFB800)",display:"flex",alignItems:"center",justifyContent:"center",fontSize:"16px"}}>✨</div>
        <div>
          <p style={{fontWeight:"800",fontSize:"15px",color:"#1A1A1A",lineHeight:1}}>Allie</p>
          <p style={{fontSize:"11px",color:"#22C55E",fontWeight:"600",marginTop:"2px"}}>● En línea</p>
        </div>
        <span style={{marginLeft:"auto",fontWeight:"900",fontSize:"17px",letterSpacing:"-0.5px",background:"linear-gradient(to right,#E4002B,#F16321)",WebkitBackgroundClip:"text",WebkitTextFillColor:"transparent"}}>túali</span>
      </div>

      <div style={{flex:1,overflowY:"auto",padding:"32px 20px",display:"flex",flexDirection:"column",position:"relative",zIndex:1}}>
        {!started ? (
          <div style={{flex:1,display:"flex",flexDirection:"column",alignItems:"center",justifyContent:"center",textAlign:"center",gap:"12px"}}>
            <div style={{width:"56px",height:"56px",borderRadius:"50%",background:"linear-gradient(135deg,#E4002B,#F16321,#FFB800)",display:"flex",alignItems:"center",justifyContent:"center",fontSize:"26px",boxShadow:"0 6px 24px rgba(228,0,43,0.25)",marginBottom:"8px"}}>✨</div>
            <h1 style={{fontSize:"28px",fontWeight:"900",color:"#1A1A1A",lineHeight:1.2}}>
              Hola, soy{" "}
              <span style={{background:"linear-gradient(to right,#E4002B,#F16321)",WebkitBackgroundClip:"text",WebkitTextFillColor:"transparent"}}>Allie</span>
            </h1>
            <p style={{fontSize:"16px",color:"#666",maxWidth:"400px",lineHeight:1.5}}>
              Basándome en tu análisis de negocio, ¿qué quieres que hagamos?
            </p>
          </div>
        ) : (
          <div style={{display:"flex",flexDirection:"column",gap:"20px",maxWidth:"720px",margin:"0 auto",width:"100%"}}>
            {messages.map((msg, i) => (
              <div key={i} className="chat-msg">
                {msg.from === "allie" ? (
                  <div style={{display:"flex",gap:"10px",alignItems:"flex-start"}}>
                    <AllieAvatar />
                    <p style={{fontSize:"15px",color:"#1A1A1A",lineHeight:1.6,paddingTop:"4px"}}>{msg.text}</p>
                  </div>
                ) : (
                  <div style={{display:"flex",justifyContent:"flex-end"}}>
                    <div style={{background:"#f4f4f4",borderRadius:"20px 4px 20px 20px",padding:"12px 18px",maxWidth:"70%"}}>
                      <p style={{fontSize:"15px",color:"#1A1A1A",lineHeight:1.5}}>{msg.text}</p>
                    </div>
                  </div>
                )}
              </div>
            ))}
            {isTyping && (
              <div className="chat-msg" style={{display:"flex",gap:"10px",alignItems:"flex-start"}}>
                <AllieAvatar />
                <div style={{background:"#f4f4f4",borderRadius:"20px",padding:"14px 18px"}}>
                  <span className="typing-dot"/><span className="typing-dot"/><span className="typing-dot"/>
                </div>
              </div>
            )}
            <div ref={bottomRef}/>
          </div>
        )}
      </div>

      <div style={{padding:"16px 20px 24px",maxWidth:"720px",margin:"0 auto",width:"100%",boxSizing:"border-box",position:"relative",zIndex:1}}>
        <div style={{display:"flex",gap:"10px",alignItems:"center",background:"rgba(255,255,255,0.8)",backdropFilter:"blur(16px)",WebkitBackdropFilter:"blur(16px)",borderRadius:"28px",border:"1px solid rgba(255,255,255,0.9)",padding:"8px 8px 8px 20px",boxShadow:"0 2px 20px rgba(0,0,0,0.07), inset 0 1px 0 rgba(255,255,255,1)"}}>
          <input
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => e.key === "Enter" && handleSend()}
            placeholder="Escribe tu mensaje..."
            style={{flex:1,border:"none",outline:"none",fontSize:"15px",fontFamily:"Nunito, sans-serif",color:"#1A1A1A",background:"transparent"}}
          />
          <button className="send-btn" onClick={handleSend} disabled={!input.trim()}>↑</button>
        </div>
        <p style={{textAlign:"center",fontSize:"11px",color:"#bbb",marginTop:"10px"}}>
          Allie puede cometer errores. Verifica la información importante.
        </p>
      </div>
    </div>
  )
}

function MetricMiniCard({ label, value }) {
  return (
    <div
      style={{
        background: "#fffaf8",
        border: "1px solid #fee2e2",
        borderRadius: "16px",
        padding: "14px 16px",
      }}
    >
      <p style={{ marginTop: 0, marginBottom: "6px", color: "#9A3412", fontSize: "11px", fontWeight: "700" }}>
        {label}
      </p>
      <p style={{ margin: 0, color: "#1A1A1A", fontSize: "22px", fontWeight: "900" }}>{value}</p>
    </div>
  )
}
