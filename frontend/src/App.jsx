import { useEffect, useState } from "react"

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000"
const DEFAULT_CLIENT_ID = "TUALI_FE_88321"
const ANALYSIS_PRESETS = {
  tuali: {
    label: "Tuali",
    selectedTools: ["tuali_profile", "available_promotions", "loyalty_status"],
  },
  yomp: {
    label: "Yomp",
    selectedTools: ["tuali_profile", "available_promotions", "loyalty_status", "yomp_growth_context"],
  },
  terminal: {
    label: "Terminal de pago",
    selectedTools: ["tuali_profile", "available_promotions", "loyalty_status"],
  },
  manual: {
    label: "Datos manuales",
    selectedTools: ["tuali_profile", "available_promotions", "loyalty_status"],
  },
}

function LiquidBackground() {
  return (
    <div className="liquid-background">
      <style>{`
        .liquid-background {
          position: fixed;
          inset: 0;
          overflow: hidden;
          z-index: 0;
          background: #fff8f3;
        }
        .liquid-layer {
          position: absolute;
          inset: -25%;
          filter: blur(80px);
          opacity: 0.95;
          animation: liquidDrift 16s ease-in-out infinite alternate;
        }
        .liquid-layer.one {
          background:
            radial-gradient(circle at 18% 28%, rgba(228,0,43,0.58), transparent 32%),
            radial-gradient(circle at 75% 25%, rgba(241,99,33,0.52), transparent 35%),
            radial-gradient(circle at 45% 78%, rgba(255,184,0,0.45), transparent 38%),
            radial-gradient(circle at 20% 82%, rgba(255,80,120,0.42), transparent 34%);
        }
        .liquid-layer.two {
          opacity: 0.7;
          filter: blur(110px);
          mix-blend-mode: multiply;
          animation: liquidDriftTwo 22s ease-in-out infinite alternate;
          background:
            radial-gradient(circle at 70% 72%, rgba(228,0,43,0.30), transparent 34%),
            radial-gradient(circle at 35% 40%, rgba(255,150,0,0.35), transparent 36%),
            radial-gradient(circle at 85% 35%, rgba(255,210,120,0.35), transparent 35%);
        }
        .soft-white-center {
          position: absolute;
          inset: 0;
          background: radial-gradient(circle at center, rgba(255,255,255,0.62), rgba(255,255,255,0.18), transparent 75%);
          pointer-events: none;
        }
        @keyframes liquidDrift {
          0% { transform: translate3d(-4%,-3%,0) scale(1) rotate(0deg); }
          50% { transform: translate3d(5%,4%,0) scale(1.16) rotate(18deg); }
          100% { transform: translate3d(-2%,6%,0) scale(1.08) rotate(-12deg); }
        }
        @keyframes liquidDriftTwo {
          0% { transform: translate3d(5%,4%,0) scale(1.08) rotate(0deg); }
          50% { transform: translate3d(-7%,-4%,0) scale(1.20) rotate(-22deg); }
          100% { transform: translate3d(3%,-5%,0) scale(1.10) rotate(16deg); }
        }
      `}</style>
      <div className="liquid-layer one" />
      <div className="liquid-layer two" />
      <div className="soft-white-center" />
    </div>
  )
}

function GlassCard({ children, style = {} }) {
  return (
    <div
      style={{
        background: "rgba(255,255,255,0.62)",
        backdropFilter: "blur(28px)",
        WebkitBackdropFilter: "blur(28px)",
        border: "1px solid rgba(255,255,255,0.5)",
        borderRadius: "24px",
        boxShadow: "0 8px 40px rgba(228,0,43,0.08), 0 2px 12px rgba(0,0,0,0.06)",
        ...style,
      }}
    >
      {children}
    </div>
  )
}

export default function App() {
  const [screen, setScreen] = useState("inicio")
  const [activePreset, setActivePreset] = useState("tuali")
  const [agentResult, setAgentResult] = useState(null)
  const [agentError, setAgentError] = useState("")
  const [isRunning, setIsRunning] = useState(false)

  useEffect(() => {
    return () => {
      setIsRunning(false)
    }
  }, [])

  async function runAnalysis(presetKey) {
    const preset = ANALYSIS_PRESETS[presetKey] ?? ANALYSIS_PRESETS.tuali

    setActivePreset(presetKey)
    setAgentResult(null)
    setAgentError("")
    setIsRunning(true)
    setScreen("procesando")

    try {
      const response = await fetch(`${API_BASE_URL}/agent/run/${DEFAULT_CLIENT_ID}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          selected_tools: preset.selectedTools,
        }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || "No se pudo generar el análisis.")
      }

      setAgentResult(data)
      setScreen("resultado")
    } catch (error) {
      setAgentError(error.message || "No se pudo conectar con Allie.")
      setScreen("resultado")
    } finally {
      setIsRunning(false)
    }
  }

  return (
    <div style={{ minHeight: "100vh", fontFamily: "Nunito, sans-serif", position: "relative" }}>
      {screen !== "inicio" && <LiquidBackground />}
      <div style={{ position: "relative", zIndex: 1 }}>
        {screen === "inicio" && <PaginaInicio onAllie={() => setScreen("bienvenido")} />}
        {screen === "bienvenido" && <PantallaBienvenido onNext={() => setScreen("herramientas")} />}
        {screen === "herramientas" && <PantallaHerramientas onChoose={runAnalysis} />}
        {screen === "procesando" && <PantallaProcesando isRunning={isRunning} activePreset={activePreset} />}
        {screen === "resultado" && (
          <PantallaResultado
            activePreset={activePreset}
            result={agentResult}
            error={agentError}
            onBack={() => setScreen("herramientas")}
          />
        )}
      </div>
    </div>
  )
}

function PaginaInicio({ onAllie }) {
  return (
    <div style={{ minHeight: "100vh", background: "white" }}>
      <div
        style={{
          background: "linear-gradient(to right, #E4002B, #F16321)",
          padding: "0 40px",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          height: "64px",
          position: "sticky",
          top: 0,
          zIndex: 100,
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: "32px" }}>
          <span style={{ color: "white", fontWeight: "900", fontSize: "26px", letterSpacing: "-1px" }}>túali</span>
          <div style={{ display: "flex", gap: "4px" }}>
            {["Inicio", "Productos", "Pedidos", "Gana"].map((tab) => (
              <button
                key={tab}
                type="button"
                style={{
                  background: "transparent",
                  border: "1px solid transparent",
                  borderRadius: "8px",
                  color: "rgba(255,255,255,0.85)",
                  padding: "6px 14px",
                  fontSize: "14px",
                  cursor: "pointer",
                  fontFamily: "Nunito, sans-serif",
                }}
              >
                {tab}
              </button>
            ))}
            <button
              type="button"
              onClick={onAllie}
              style={{
                background: "rgba(255,255,255,0.22)",
                border: "1px solid rgba(255,255,255,0.55)",
                borderRadius: "8px",
                color: "white",
                padding: "6px 16px",
                fontSize: "14px",
                fontWeight: "700",
                cursor: "pointer",
                fontFamily: "Nunito, sans-serif",
                transition: "all 0.2s",
              }}
              onMouseEnter={(event) => {
                event.currentTarget.style.background = "rgba(255,255,255,0.38)"
              }}
              onMouseLeave={(event) => {
                event.currentTarget.style.background = "rgba(255,255,255,0.22)"
              }}
            >
              ✨ Allie
            </button>
          </div>
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
          <div
            style={{
              background: "rgba(255,255,255,0.15)",
              borderRadius: "20px",
              padding: "6px 16px",
              display: "flex",
              alignItems: "center",
              gap: "8px",
              width: "200px",
            }}
          >
            <span style={{ color: "rgba(255,255,255,0.7)" }}>🔍</span>
            <span style={{ color: "rgba(255,255,255,0.6)", fontSize: "14px" }}>Buscar</span>
          </div>
          <div
            style={{
              width: "36px",
              height: "36px",
              borderRadius: "50%",
              background: "white",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontWeight: "700",
              color: "#E4002B",
              fontSize: "12px",
            }}
          >
            AC
          </div>
        </div>
      </div>

      <div
        style={{
          background: "white",
          padding: "8px 40px",
          borderBottom: "1px solid #eee",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <div>
          <span style={{ fontSize: "12px", color: "#999" }}>Punto de venta: </span>
          <span style={{ fontSize: "13px", fontWeight: "700" }}>Abarrotes Chabelita</span>
          <span style={{ fontSize: "12px", color: "#999" }}> · Mar ártico no.201, Mazatlán</span>
        </div>
        <span
          style={{
            fontSize: "12px",
            background: "#e8f5e9",
            color: "#22C55E",
            padding: "3px 12px",
            borderRadius: "10px",
            fontWeight: "600",
          }}
        >
          ● Pedido Confirmado · #39E2C00A
        </span>
      </div>

      <div style={{ maxWidth: "1200px", margin: "0 auto", padding: "28px 40px" }}>
        <div style={{ display: "flex", gap: "10px", marginBottom: "24px" }}>
          <div style={{ background: "#E4002B", borderRadius: "10px", padding: "10px 24px" }}>
            <span style={{ color: "white", fontWeight: "900", fontSize: "18px" }}>Coca-Cola</span>
          </div>
          <div style={{ background: "#f5e6c8", borderRadius: "10px", padding: "10px 24px" }}>
            <span style={{ color: "#8B6914", fontWeight: "700", fontSize: "18px" }}>Bokados</span>
          </div>
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "2fr 1fr", gap: "20px", marginBottom: "24px" }}>
          <div
            onClick={onAllie}
            style={{
              background: "linear-gradient(135deg, #fff0f0, #fff5ee)",
              borderRadius: "20px",
              padding: "36px",
              border: "2px solid rgba(228,0,43,0.1)",
              cursor: "pointer",
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              transition: "all 0.2s ease",
            }}
            onMouseEnter={(event) => {
              event.currentTarget.style.transform = "scale(1.01)"
              event.currentTarget.style.boxShadow = "0 16px 50px rgba(228,0,43,0.15)"
            }}
            onMouseLeave={(event) => {
              event.currentTarget.style.transform = "scale(1)"
              event.currentTarget.style.boxShadow = "none"
            }}
          >
            <div>
              <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "10px" }}>
                <span style={{ fontSize: "28px" }}>✨</span>
                <span
                  style={{
                    fontWeight: "900",
                    fontSize: "30px",
                    background: "linear-gradient(to right, #E4002B, #F16321)",
                    WebkitBackgroundClip: "text",
                    WebkitTextFillColor: "transparent",
                  }}
                >
                  Allie
                </span>
              </div>
              <p style={{ fontWeight: "700", fontSize: "20px", color: "#1A1A1A", marginBottom: "8px" }}>
                Tu asistente de crecimiento
              </p>
              <p style={{ fontSize: "14px", color: "#666", marginBottom: "24px", maxWidth: "340px" }}>
                Recibe recomendaciones personalizadas basadas en tu historial de Tuali para hacer crecer tu negocio.
              </p>
              <button
                type="button"
                style={{
                  background: "linear-gradient(to right, #E4002B, #F16321)",
                  border: "none",
                  borderRadius: "12px",
                  padding: "13px 26px",
                  color: "white",
                  fontWeight: "700",
                  cursor: "pointer",
                  fontSize: "14px",
                  fontFamily: "Nunito, sans-serif",
                }}
              >
                Comenzar con Allie →
              </button>
            </div>
            <div style={{ fontSize: "100px", userSelect: "none" }}>🤖</div>
          </div>

          <div
            style={{
              background: "linear-gradient(135deg, #fff8e1, #fff3cd)",
              borderRadius: "20px",
              padding: "28px",
              border: "1px solid rgba(255,184,0,0.2)",
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-between",
            }}
          >
            <div>
              <p
                style={{
                  fontSize: "20px",
                  fontWeight: "900",
                  color: "#E4002B",
                  lineHeight: "1.3",
                  marginBottom: "8px",
                }}
              >
                ¡Ya acumulaste Puntos, ahora hazlos valer!
              </p>
              <p style={{ fontSize: "13px", color: "#888", marginBottom: "20px" }}>
                Canjea por productos Coca-Cola.
              </p>
            </div>
            <div
              style={{
                background: "linear-gradient(to right, #E4002B, #F16321)",
                borderRadius: "10px",
                padding: "8px 18px",
                display: "inline-block",
                width: "fit-content",
              }}
            >
              <span style={{ color: "white", fontWeight: "900", fontSize: "18px" }}>gana</span>
            </div>
          </div>
        </div>

        <div
          style={{
            background: "white",
            borderRadius: "16px",
            padding: "22px 28px",
            marginBottom: "20px",
            boxShadow: "0 2px 12px rgba(0,0,0,0.06)",
          }}
        >
          <h3 style={{ fontWeight: "700", fontSize: "16px", marginBottom: "18px" }}>Categorías</h3>
          <div style={{ display: "flex", gap: "20px" }}>
            {[
              { icon: "👑", label: "Tus más vendidos" },
              { icon: "🏷️", label: "Promos", active: true },
              { icon: "🥤", label: "Refrescos" },
              { icon: "💧", label: "Agua" },
              { icon: "🥛", label: "Lácteos" },
              { icon: "🧃", label: "Jugos" },
              { icon: "⚡", label: "Energéticas" },
            ].map((category) => (
              <div
                key={category.label}
                style={{
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  gap: "8px",
                  cursor: "pointer",
                }}
              >
                <div
                  style={{
                    width: "64px",
                    height: "64px",
                    borderRadius: "14px",
                    border: category.active ? "2px solid #E4002B" : "1px solid #eee",
                    background: "white",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    fontSize: "28px",
                  }}
                >
                  {category.icon}
                </div>
                <span
                  style={{
                    fontSize: "11px",
                    textAlign: "center",
                    fontWeight: category.active ? "700" : "400",
                    color: category.active ? "#E4002B" : "#666",
                  }}
                >
                  {category.label}
                </span>
              </div>
            ))}
          </div>
        </div>

        <div
          style={{
            background: "white",
            borderRadius: "16px",
            padding: "22px 28px",
            boxShadow: "0 2px 12px rgba(0,0,0,0.06)",
          }}
        >
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
              <span style={{ fontSize: "26px" }}>🧺</span>
              <div>
                <p style={{ fontWeight: "700", fontSize: "15px" }}>Vuelve a surtir</p>
                <p style={{ fontSize: "13px", color: "#999" }}>De pedidos anteriores, listos para reponer.</p>
              </div>
            </div>
            <span style={{ color: "#E4002B", fontSize: "13px", fontWeight: "600", cursor: "pointer" }}>Ver todos ›</span>
          </div>
        </div>
      </div>
    </div>
  )
}

function PantallaBienvenido({ onNext }) {
  const [phase, setPhase] = useState("bienvenido")

  useEffect(() => {
    const timeoutId = setTimeout(() => setPhase("subtitle"), 2500)
    return () => clearTimeout(timeoutId)
  }, [])

  return (
    <div
      style={{
        position: "fixed",
        inset: 0,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        zIndex: 50,
      }}
    >
      <style>{`
        @keyframes fadeInUp {
          from { opacity:0; transform:translateY(40px); }
          to { opacity:1; transform:translateY(0); }
        }
      `}</style>
      <div style={{ textAlign: "center", padding: "0 40px" }}>
        {phase === "bienvenido" && (
          <h1
            style={{
              fontSize: "clamp(64px,10vw,110px)",
              fontWeight: "900",
              color: "#1A1A1A",
              letterSpacing: "-3px",
              lineHeight: "1",
              animation: "fadeInUp 0.9s ease forwards",
            }}
          >
            Bienvenido
          </h1>
        )}
        {phase === "subtitle" && (
          <div style={{ animation: "fadeInUp 0.8s ease forwards" }}>
            <p
              style={{
                fontSize: "clamp(24px,3.5vw,40px)",
                fontWeight: "400",
                color: "#1A1A1A",
                lineHeight: "1.35",
                maxWidth: "560px",
                margin: "0 auto 48px",
              }}
            >
              Empecemos con tu análisis de negocio
            </p>
            <button
              type="button"
              onClick={onNext}
              style={{
                background: "linear-gradient(to right, #E4002B, #F16321)",
                border: "none",
                borderRadius: "50px",
                padding: "16px 48px",
                fontSize: "18px",
                fontWeight: "700",
                color: "white",
                cursor: "pointer",
                fontFamily: "Nunito, sans-serif",
                boxShadow: "0 8px 32px rgba(228,0,43,0.28)",
                transition: "all 0.2s",
              }}
              onMouseEnter={(event) => {
                event.currentTarget.style.transform = "scale(1.05)"
              }}
              onMouseLeave={(event) => {
                event.currentTarget.style.transform = "scale(1)"
              }}
            >
              Continuar →
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

function PantallaHerramientas({ onChoose }) {
  const btnBase = {
    width: "100%",
    padding: "15px 18px",
    borderRadius: "14px",
    border: "1.5px solid rgba(228,0,43,0.4)",
    background: "rgba(255,255,255,0.5)",
    backdropFilter: "blur(12px)",
    color: "#1A1A1A",
    fontWeight: "600",
    fontSize: "15px",
    cursor: "pointer",
    fontFamily: "Nunito, sans-serif",
    transition: "all 0.2s",
    textAlign: "left",
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
  }

  return (
    <div
      style={{
        position: "fixed",
        inset: 0,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        zIndex: 50,
      }}
    >
      <style>{`
        @keyframes fadeInUp {
          from { opacity:0; transform:translateY(30px) }
          to { opacity:1; transform:translateY(0) }
        }
      `}</style>
      <GlassCard style={{ padding: "40px", maxWidth: "500px", width: "90%", animation: "fadeInUp 0.6s ease forwards" }}>
        <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "10px" }}>
          <span
            style={{
              fontWeight: "900",
              fontSize: "20px",
              background: "linear-gradient(to right, #E4002B, #F16321)",
              WebkitBackgroundClip: "text",
              WebkitTextFillColor: "transparent",
            }}
          >
            ✨ Allie
          </span>
        </div>
        <p style={{ fontSize: "16px", fontWeight: "700", color: "#1A1A1A", marginBottom: "6px", lineHeight: "1.4" }}>
          Para generar el análisis de tu negocio, utilizo tu información en Tuali.
        </p>
        <p style={{ fontSize: "14px", color: "#666", marginBottom: "24px", lineHeight: "1.5" }}>
          ¿Te gustaría complementar el análisis con alguna de estas herramientas de ventas?
        </p>
        <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
          <button
            type="button"
            onClick={() => onChoose("tuali")}
            style={{
              ...btnBase,
              background: "linear-gradient(to right, #E4002B, #F16321)",
              color: "white",
              border: "none",
              backdropFilter: "none",
            }}
            onMouseEnter={(event) => {
              event.currentTarget.style.transform = "scale(1.02)"
            }}
            onMouseLeave={(event) => {
              event.currentTarget.style.transform = "scale(1)"
            }}
          >
            <span>Continuar solo con Tuali</span>
            <span>→</span>
          </button>
          {[
            { label: "Yomp!", preset: "yomp" },
            { label: "Terminal de pago", preset: "terminal" },
            { label: "Ingresar datos manualmente", preset: "manual" },
          ].map((option) => (
            <button
              key={option.label}
              type="button"
              onClick={() => onChoose(option.preset)}
              style={btnBase}
              onMouseEnter={(event) => {
                event.currentTarget.style.background = "rgba(228,0,43,0.08)"
                event.currentTarget.style.borderColor = "#E4002B"
              }}
              onMouseLeave={(event) => {
                event.currentTarget.style.background = "rgba(255,255,255,0.5)"
                event.currentTarget.style.borderColor = "rgba(228,0,43,0.4)"
              }}
            >
              <span>{option.label}</span>
              <span style={{ color: "#E4002B" }}>→</span>
            </button>
          ))}
        </div>
      </GlassCard>
    </div>
  )
}

function PantallaProcesando({ isRunning, activePreset }) {
  const activeLabel = ANALYSIS_PRESETS[activePreset]?.label ?? "Tuali"

  return (
    <div
      style={{
        position: "fixed",
        inset: 0,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        zIndex: 50,
      }}
    >
      <style>{`
        .fluid-orb-wrapper {
          position: relative;
          width: 300px;
          height: 300px;
          display: flex;
          align-items: center;
          justify-content: center;
        }
        .fluid-orb-glow {
          position: absolute;
          width: 360px;
          height: 360px;
          border-radius: 999px;
          background: radial-gradient(circle, rgba(255,184,0,0.45), rgba(241,99,33,0.25), rgba(228,0,43,0.12), transparent 70%);
          filter: blur(45px);
          animation: glowBreath 4s ease-in-out infinite;
        }
        .fluid-orb {
          position: relative;
          width: 250px;
          height: 250px;
          overflow: hidden;
          border-radius: 54% 46% 48% 52% / 48% 55% 45% 52%;
          background:
            radial-gradient(circle at 32% 62%, rgba(220,40,130,0.82), transparent 34%),
            radial-gradient(circle at 48% 48%, rgba(255,75,120,0.74), transparent 40%),
            radial-gradient(circle at 35% 32%, rgba(255,140,20,0.85), transparent 34%),
            radial-gradient(circle at 72% 35%, rgba(255,225,120,0.82), transparent 42%),
            radial-gradient(circle at 75% 72%, rgba(255,240,160,0.72), transparent 44%);
          filter: blur(0.2px);
          animation: orbMorph 7s ease-in-out infinite, orbFloat 8s ease-in-out infinite;
          box-shadow: 0 24px 90px rgba(228,0,43,0.18), 0 0 110px rgba(255,184,0,0.25);
        }
        .fluid-orb::before {
          content: "";
          position: absolute;
          inset: -35%;
          background:
            radial-gradient(circle at 42% 55%, rgba(255,40,130,0.75), transparent 30%),
            radial-gradient(circle at 35% 28%, rgba(255,130,20,0.85), transparent 28%),
            radial-gradient(circle at 76% 32%, rgba(255,230,120,0.80), transparent 42%);
          filter: blur(22px);
          animation: innerFlowA 5.5s ease-in-out infinite;
          mix-blend-mode: screen;
        }
        .fluid-orb::after {
          content: "";
          position: absolute;
          inset: -30%;
          background:
            radial-gradient(circle at 55% 55%, rgba(220,60,150,0.65), transparent 36%),
            radial-gradient(circle at 75% 38%, rgba(255,220,95,0.74), transparent 44%);
          filter: blur(26px);
          animation: innerFlowB 6.8s ease-in-out infinite;
          mix-blend-mode: multiply;
        }
        .orb-soft-mask {
          position: absolute;
          inset: 0;
          border-radius: inherit;
          background: radial-gradient(circle at 50% 50%, transparent 30%, rgba(255,255,255,0.18) 100%);
          pointer-events: none;
        }
        @keyframes orbMorph {
          0%   { border-radius: 52% 48% 45% 55% / 50% 45% 55% 50%; }
          25%  { border-radius: 58% 42% 54% 46% / 42% 58% 45% 55%; }
          50%  { border-radius: 45% 55% 60% 40% / 58% 42% 52% 48%; }
          75%  { border-radius: 60% 40% 42% 58% / 45% 55% 58% 42%; }
          100% { border-radius: 52% 48% 45% 55% / 50% 45% 55% 50%; }
        }
        @keyframes orbFloat {
          0%,100% { transform: translateY(0) scale(1); }
          50% { transform: translateY(-8px) scale(1.03); }
        }
        @keyframes innerFlowA {
          0% { transform: translate(-12%,6%) rotate(0deg) scale(1); }
          50% { transform: translate(12%,-10%) rotate(55deg) scale(1.25); }
          100% { transform: translate(-12%,6%) rotate(0deg) scale(1); }
        }
        @keyframes innerFlowB {
          0% { transform: translate(10%,-6%) rotate(0deg) scale(1.1); }
          50% { transform: translate(-12%,12%) rotate(-70deg) scale(1.35); }
          100% { transform: translate(10%,-6%) rotate(0deg) scale(1.1); }
        }
        @keyframes glowBreath {
          0%,100% { opacity: 0.52; transform: scale(0.95); }
          50% { opacity: 0.85; transform: scale(1.12); }
        }
        @keyframes fadeInUp {
          from { opacity:0; transform:translateY(18px); }
          to { opacity:1; transform:translateY(0); }
        }
      `}</style>

      <div className="fluid-orb-wrapper">
        <div className="fluid-orb-glow" />
        <div className="fluid-orb">
          <div className="orb-soft-mask" />
        </div>
      </div>

      <div style={{ textAlign: "center", marginTop: "42px", animation: "fadeInUp 0.8s ease 0.3s both" }}>
        <p style={{ fontSize: "22px", fontWeight: "800", color: "#1A1A1A", marginBottom: "10px" }}>
          {isRunning ? `Estoy generando tu análisis con ${activeLabel}` : "Preparando el resultado"}
        </p>
        <p style={{ fontSize: "15px", color: "#777" }}>
          {activePreset === "yomp"
            ? "Voy a consultar ventas e inventario de Yomp para construir el análisis."
            : "Esto tomará solo unos segundos"}
        </p>
      </div>
    </div>
  )
}

function PantallaResultado({ activePreset, result, error, onBack }) {
  const activeLabel = ANALYSIS_PRESETS[activePreset]?.label ?? "Tuali"

  return (
    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        padding: "48px 20px",
      }}
    >
      <GlassCard style={{ maxWidth: "820px", width: "100%", padding: "36px" }}>
        <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "14px" }}>
          <span style={{ fontSize: "24px" }}>✨</span>
          <span
            style={{
              fontWeight: "900",
              fontSize: "22px",
              background: "linear-gradient(to right, #E4002B, #F16321)",
              WebkitBackgroundClip: "text",
              WebkitTextFillColor: "transparent",
            }}
          >
            Allie
          </span>
        </div>

        <div
          style={{
            display: "inline-flex",
            alignItems: "center",
            gap: "8px",
            background: "#fff1f2",
            color: "#be123c",
            borderRadius: "999px",
            padding: "8px 14px",
            fontSize: "12px",
            fontWeight: "700",
            marginBottom: "18px",
          }}
        >
          Análisis corrido con {activeLabel}
        </div>

        {error ? (
          <>
            <h2 style={{ marginTop: 0, marginBottom: "10px", color: "#991B1B", fontSize: "32px" }}>
              No se pudo generar el análisis
            </h2>
            <p style={{ color: "#7F1D1D", lineHeight: "1.6", marginBottom: "24px" }}>{error}</p>
          </>
        ) : (
          <>
            <h2 style={{ marginTop: 0, marginBottom: "10px", color: "#1A1A1A", fontSize: "32px" }}>
              {result?.summary?.store_name ?? "Resultado listo"}
            </h2>
            <p style={{ color: "#525252", lineHeight: "1.6", marginBottom: "14px" }}>
              {result?.message ?? "Allie terminó tu análisis."}
            </p>
            <div
              style={{
                background: "#fff7ed",
                border: "1px solid #fdba74",
                borderRadius: "18px",
                padding: "18px 20px",
                marginBottom: "24px",
              }}
            >
              <p style={{ margin: 0, color: "#9A3412", fontWeight: "700", lineHeight: "1.5" }}>
                {result?.summary?.headline ?? "No hay resumen disponible."}
              </p>
            </div>

            <div
              style={{
                display: "grid",
                gridTemplateColumns: "repeat(3, minmax(0, 1fr))",
                gap: "12px",
                marginBottom: "24px",
              }}
            >
              <MetricMiniCard
                label="Ticket promedio"
                value={result?.summary?.ticket_average != null ? `$${result.summary.ticket_average}` : "-"}
              />
              <MetricMiniCard
                label="Meta del día"
                value={result?.summary?.goal_progress != null ? `${result.summary.goal_progress}%` : "-"}
              />
              <MetricMiniCard
                label="Stock crítico"
                value={String(result?.summary?.critical_stock_count ?? 0)}
              />
            </div>

            <div style={{ marginBottom: "24px" }}>
              <p style={{ fontWeight: "800", color: "#1A1A1A", marginBottom: "12px" }}>Recomendaciones</p>
              <div style={{ display: "grid", gap: "12px" }}>
                {(result?.recommendations ?? []).map((recommendation) => (
                  <div
                    key={`${recommendation.signal}-${recommendation.title}`}
                    style={{
                      border: "1px solid #f1f5f9",
                      borderRadius: "16px",
                      padding: "16px 18px",
                      background: "white",
                    }}
                  >
                    <div style={{ display: "flex", justifyContent: "space-between", gap: "12px", marginBottom: "6px" }}>
                      <span style={{ fontWeight: "700", color: "#1A1A1A" }}>{recommendation.title}</span>
                      <span
                        style={{
                          fontSize: "11px",
                          color: "#E4002B",
                          fontWeight: "800",
                          textTransform: "uppercase",
                        }}
                      >
                        {recommendation.priority}
                      </span>
                    </div>
                    <p style={{ margin: 0, color: "#666", fontSize: "14px", lineHeight: "1.6" }}>
                      {recommendation.detail}
                    </p>
                  </div>
                ))}
              </div>
            </div>

            <div
              style={{
                display: "flex",
                flexWrap: "wrap",
                gap: "10px",
                marginBottom: "24px",
              }}
            >
              {(result?.data_sources ?? []).map((source) => (
                <span
                  key={source.source}
                  style={{
                    fontSize: "12px",
                    fontWeight: "700",
                    padding: "8px 12px",
                    borderRadius: "999px",
                    background: source.connected ? "#ecfdf5" : "#fff7ed",
                    color: source.connected ? "#166534" : "#9A3412",
                    border: source.connected ? "1px solid #bbf7d0" : "1px solid #fdba74",
                  }}
                >
                  {source.source} {source.mode ? `(${source.mode})` : ""}
                </span>
              ))}
            </div>
          </>
        )}

        <button
          type="button"
          onClick={onBack}
          style={{
            background: "linear-gradient(to right, #E4002B, #F16321)",
            border: "none",
            borderRadius: "50px",
            padding: "14px 28px",
            fontSize: "16px",
            fontWeight: "700",
            color: "white",
            cursor: "pointer",
            fontFamily: "Nunito, sans-serif",
          }}
        >
          Volver
        </button>
      </GlassCard>
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
