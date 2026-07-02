use serde::Serialize;
use tauri::Manager;

// Структура для возврата успешного результата во фронтенд
#[derive(Debug, Serialize)]
pub struct PortalResult {
    x: i32,
    z: i32,
}

// Вспомогательная функция перевода угла в декартов
fn decart(angle: f64) -> f64 {
    angle + 90.0
}

// Проверка направления луча
fn check_condition(angle: f64, x: f64, z: f64, c_x: f64, c_z: f64) -> bool {
    let rad = decart(angle).to_radians();
    let sina = rad.sin().round();
    let cosa = rad.cos().round();

    if cosa >= 0.0 && cosa <= 1.0 && sina >= 0.0 && sina < 1.0 {
        x >= c_x
    } else if cosa > -1.0 && cosa <= 0.0 && sina >= 0.0 && sina <= 1.0 {
        z >= c_z
    } else if cosa >= -1.0 && cosa <= 0.0 && sina > -1.0 && sina <= 0.0 {
        x <= c_x
    } else if cosa >= 0.0 && cosa < 1.0 && sina >= -1.0 && sina <= 0.0 {
        z <= c_z
    } else {
        false
    }
}

// КОМАНДА РАСЧЕТА КООРДИНАТ ПОРТАЛА
#[tauri::command]
fn calculate_portal(
    x1: f64, z1: f64, alpha: f64,
    x2: f64, z2: f64, beta: f64
) -> Result<PortalResult, String> {
    
    // 1. Проверка на параллельность лучей
    if decart(alpha) == decart(beta) {
        return Err("error_parallel".into());
    }

    let rad_alpha = decart(alpha).to_radians();
    let rad_beta = decart(beta).to_radians();
    
    let tan_alpha = rad_alpha.tan();
    let tan_beta = rad_beta.tan();

    // 2. Расчет точки пересечения прямых
    let x = (z2 - z1 + tan_alpha * x1 - tan_beta * x2) / (tan_alpha - tan_beta);
    let z = ((x1 - x2) * tan_alpha * tan_beta + tan_alpha * z2 - tan_beta * z1) / (tan_alpha - tan_beta);

    // 3. Проверка выхода за границы мира Minecraft
    if !( -29999984.0..=29999983.0 ).contains(&x) || !( -29999984.0..=29999983.0 ).contains(&z) {
        return Err("error_out".into());
    }

    // 4. Проверка, что пересечение лежит ПО НАПРАВЛЕНИЮ броска
    if check_condition(alpha, x, z, x1, z1) && check_condition(beta, x, z, x2, z2) {
        unsafe {
            Ok(PortalResult {
                x: x.to_int_unchecked::<i32>(),
                z: z.to_int_unchecked::<i32>(),
            })
        }
    } else {
        Err("error_intersection".into())
    }
}

// 5. ПОЛУЧЕНИЕ СИСТЕМНОГО АКЦЕНТА ДЛЯ WINUI 3
#[tauri::command]
fn get_accent_color() -> Result<String, String> {
    #[cfg(target_os = "windows")]
    {
        use winreg::enums::HKEY_CURRENT_USER;
        use winreg::RegKey;

        let hkcu = RegKey::predef(HKEY_CURRENT_USER);
        if let Ok(dwm_key) = hkcu.open_subkey("Software\\Microsoft\\Windows\\DWM") {
            if let Ok(colorization) = dwm_key.get_value::<u32, _>("ColorizationColor") {
                let r = ((colorization >> 16) & 0xFF) as u8;
                let g = ((colorization >> 8) & 0xFF) as u8;
                let b = (colorization & 0xFF) as u8;
                return Ok(format!("#{:02X}{:02X}{:02X}", r, g, b));
            }
        }
    }
    Ok("#0078D4".to_string())
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_opener::init())
        .setup(|app| {
            if let Some(window) = app.get_webview_window("main") {
                let _ = window.set_min_size(Some(tauri::Size::Logical(tauri::LogicalSize {
                    width: 560.0,
                    height: 440.0,
                })));

                #[cfg(target_os = "windows")]
                {
                    use window_vibrancy::apply_mica;
                    let window_clone = window.clone();
                    let _ = window.run_on_main_thread(move || {
                        // Точно как в твоем PDF-Converter проекте
                        let _ = apply_mica(&window_clone, None);
                        let _ = window_clone.show();
                    });
                }
                
                #[cfg(not(target_os = "windows"))]
                {
                    let _ = window.show();
                }
            }
            Ok(())
        })
        .invoke_handler(tauri::generate_handler![
            calculate_portal,
            get_accent_color
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}