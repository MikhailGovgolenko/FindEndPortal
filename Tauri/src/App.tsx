import { useState, useEffect } from "react";
import { invoke } from "@tauri-apps/api/core";

const translations = {
  ru: {
    first_eye: "Первое Око Эндера",
    second_eye: "Второе Око Эндера",
    label_coordinates: "Координаты Крепости",
    btn_command: "Копировать команду /tp",
    btn_clear: "Очистить поля",
    alpha: "Угол броска 1",
    beta: "Угол броска 2",
    paste: "Вставить из F3+C",
    error: "Ошибка",
    error_parallel: "Лучи параллельны",
    error_intersection: "Лучи не пересекаются",
    error_out: "За границами мира",
  },
  en: {
    first_eye: "First Eye of Ender",
    second_eye: "Second Eye of Ender",
    label_coordinates: "Stronghold Coordinates",
    btn_command: "Copy /tp command",
    btn_clear: "Clear Fields",
    alpha: "Throw Angle 1",
    beta: "Throw Angle 2",
    paste: "Paste from F3+C",
    error: "Error",
    error_parallel: "Rays are parallel",
    error_intersection: "Rays do not intersect",
    error_out: "Out of bounds",
  },
};

const getSystemLanguage = (): "ru" | "en" => {
  const navLang = navigator.language || "en";
  return navLang.toLowerCase().startsWith("ru") ? "ru" : "en";
};

const isTauri = !!(window as any).__TAURI_INTERNALS__;

/**
 * Математический расчет пересечения двух лучей (Ока Эндера) на клиенте.
 * В Minecraft угол (yaw) считается от оси Z (0 = юг, 90 = запад, 180 = север, -90/270 = восток).
 */
function calculatePortalInJs(
  x1: number,
  z1: number,
  alpha: number,
  x2: number,
  z2: number,
  beta: number,
): { x: number; z: number } {
  // Переводим углы Minecraft в радианы для стандартной декартовой системы.
  // В Minecraft: X_dir = -sin(yaw), Z_dir = cos(yaw)
  const rad1 = (alpha * Math.PI) / 180.0;
  const rad2 = (beta * Math.PI) / 180.0;

  const dx1 = -Math.sin(rad1);
  const dz1 = Math.cos(rad1);

  const dx2 = -Math.sin(rad2);
  const dz2 = Math.cos(rad2);

  // Определитель матрицы (проверка на параллельность)
  const det = dx1 * dz2 - dz1 * dx2;

  if (Math.abs(det) < 1e-5) {
    throw "error_parallel";
  }

  // Находим параметры пересечения лучей t1 и t2
  const t1 = ((x2 - x1) * dz2 - (z2 - z1) * dx2) / det;
  const t2 = ((x2 - x1) * dz1 - (z2 - z1) * dx1) / det;

  // Если t1 или t2 меньше нуля, значит лучи пересекаются «сзади» (в противоположную сторону от броска)
  if (t1 < 0 || t2 < 0) {
    throw "error_intersection";
  }

  // Точка пересечения
  const resX = x1 + t1 * dx1;
  const resZ = z1 + t1 * dz1;

  // Проверка на лимиты мира Minecraft (±30,000,000)
  if (Math.abs(resX) > 30000000 || Math.abs(resZ) > 30000000) {
    throw "error_out";
  }

  return { x: Math.round(resX), z: Math.round(resZ) };
}

export default function App() {
  const lang = getSystemLanguage();
  const t = translations[lang];

  const [x1, setX1] = useState("");
  const [z1, setZ1] = useState("");
  const [alpha, setAlpha] = useState("");

  const [x2, setX2] = useState("");
  const [z2, setZ2] = useState("");
  const [beta, setBeta] = useState("");

  const [resX, setResX] = useState<string>("");
  const [resZ, setResZ] = useState<string>("");

  // Синхронизация системного акцентного цвета Windows, сброс фона для Mica и блокировка веб-контекста
  useEffect(() => {
    if (isTauri) {
      // Добавляем маркер приложения для стилей
      document.body.classList.add("is-tauri");
  
      document.documentElement.style.setProperty("--winui-window-bg", "transparent");
      
      const updateAccentColor = async () => {
        try {
          const systemHex = await invoke<string>("get_accent_color");
          document.documentElement.style.setProperty("--winui-accent-system", systemHex);
        } catch (err) {
          console.warn("System accent color integration skipped.");
        }
      };
  
      updateAccentColor();
      window.addEventListener("focus", updateAccentColor);
      return () => window.removeEventListener("focus", updateAccentColor);
    }
  }, []);

  useEffect(() => {
    const handleContextMenu = (e: MouseEvent) => e.preventDefault();
    document.addEventListener("contextmenu", handleContextMenu);
    return () => document.removeEventListener("contextmenu", handleContextMenu);
  }, []);

  // Вычисление точки пересечения лучей прямо в браузере / клиенте
  useEffect(() => {
    const numX1 = parseFloat(x1);
    const numZ1 = parseFloat(z1);
    const numAlpha = parseFloat(alpha);
    const numX2 = parseFloat(x2);
    const numZ2 = parseFloat(z2);
    const numBeta = parseFloat(beta);

    if (
      isNaN(numX1) ||
      isNaN(numZ1) ||
      isNaN(numAlpha) ||
      isNaN(numX2) ||
      isNaN(numZ2) ||
      isNaN(numBeta)
    ) {
      setResX("");
      setResZ("");
      return;
    }

    try {
      const result = calculatePortalInJs(
        numX1,
        numZ1,
        numAlpha,
        numX2,
        numZ2,
        numBeta,
      );
      setResX(result.x.toString());
      setResZ(result.z.toString());
    } catch (err: any) {
      setResX(t.error);
      setResZ((t as any)[err] || String(err));
    }
  }, [x1, z1, alpha, x2, z2, beta, t.error]);

  const parseMinecraftClipboard = (
    text: string,
    setX: (v: string) => void,
    setZ: (v: string) => void,
    setAngle: (v: string) => void,
  ) => {
    const parts = text.trim().split(/\s+/);
    if (parts.length >= 10 && parts[4] === "tp") {
      setX(parts[6]);
      setZ(parts[8]);
      setAngle((parseFloat(parts[9]) % 360).toFixed(2));
    }
  };

  const handlePaste1 = async () => {
    try {
      const text = await navigator.clipboard.readText();
      parseMinecraftClipboard(text, setX1, setZ1, setAlpha);
    } catch (e) {
      console.error("Failed to read clipboard", e);
    }
  };

  const handlePaste2 = async () => {
    try {
      const text = await navigator.clipboard.readText();
      parseMinecraftClipboard(text, setX2, setZ2, setBeta);
    } catch (e) {
      console.error("Failed to read clipboard", e);
    }
  };

  return (
    <div className="app-container">
      <div className="app-content-wrapper">
        <div className="input-grid">
          {/* Блок первого глаза */}
          <div className="win-card">
            <div className="card-title">{t.first_eye}</div>
            <div className="input-group">
              <input
                className="win-input"
                placeholder="X"
                value={x1}
                onChange={(e) => setX1(e.target.value)}
              />
              <input
                className="win-input"
                placeholder="Z"
                value={z1}
                onChange={(e) => setZ1(e.target.value)}
              />
              <input
                className="win-input"
                placeholder={t.alpha}
                value={alpha}
                onChange={(e) => setAlpha(e.target.value)}
              />
            </div>
            <button
              className="btn btn-standard"
              style={{ marginTop: "12px", width: "100%" }}
              onClick={handlePaste1}
            >
              {t.paste}
            </button>
          </div>

          {/* Блок второго глаза */}
          <div className="win-card">
            <div className="card-title">{t.second_eye}</div>
            <div className="input-group">
              <input
                className="win-input"
                placeholder="X"
                value={x2}
                onChange={(e) => setX2(e.target.value)}
              />
              <input
                className="win-input"
                placeholder="Z"
                value={z2}
                onChange={(e) => setZ2(e.target.value)}
              />
              <input
                className="win-input"
                placeholder={t.beta}
                value={beta}
                onChange={(e) => setBeta(e.target.value)}
              />
            </div>
            <button
              className="btn btn-standard"
              style={{ marginTop: "12px", width: "100%" }}
              onClick={handlePaste2}
            >
              {t.paste}
            </button>
          </div>
        </div>

        {/* Карточка вывода */}
        <div className="win-card result-card">
          <div className="card-title">{t.label_coordinates}</div>
          <div className="result-row">
            <div>
              X: <span className="result-value">{resX || "—"}</span>
            </div>
            <div>
              Z: <span className="result-value">{resZ || "—"}</span>
            </div>
          </div>
        </div>

        {/* Панель действий */}
        <div className="actions-layout">
          <button
            className="btn btn-accent"
            style={{ flexGrow: 1 }}
            disabled={!resX || resX === t.error}
            onClick={() =>
              navigator.clipboard.writeText(`tp @s ${resX} ~ ${resZ}`)
            }
          >
            {t.btn_command}
          </button>
          <button
            className="btn btn-standard"
            onClick={() => {
              setX1("");
              setZ1("");
              setAlpha("");
              x2 && setX2("");
              z2 && setZ2("");
              beta && setBeta("");
              setResX("");
              setResZ("");
            }}
          >
            {t.btn_clear}
          </button>
        </div>
      </div>
    </div>
  );
}
