import re

with open('templates/index.html', 'r') as f:
    content = f.read()

new_css = """
        :root {
            --primary: #0ea5e9; /* Sky blue, friendly and trustworthy */
            --primary-dark: #0284c7;
            --danger: #ef4444; /* Alert Red */
            --success: #22c55e; /* Action Green */
            --warning: #f59e0b;
            --bg-light: #f1f5f9; /* Very soft blue-gray */
            --card-bg: #ffffff;
            --text-dark: #1e293b; /* Deep slate */
            --text-muted: #64748b;
            --border: #e2e8f0;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: "Quicksand", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }

        body {
            background-color: var(--bg-light);
            color: var(--text-dark);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        header {
            background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
            padding: 1.5rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            color: white;
            box-shadow: 0 4px 15px rgba(14, 165, 233, 0.3);
            border-bottom-left-radius: 20px;
            border-bottom-right-radius: 20px;
            margin-bottom: 1rem;
        }
        
        header h1 {
            font-size: 1.5rem;
            font-weight: 800;
        }

        .badge-academic {
            background: white;
            color: var(--primary-dark);
            padding: 0.4rem 0.8rem;
            border-radius: 9999px;
            font-size: 0.85rem;
            font-weight: 800;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }

        .nav-tabs {
            display: flex;
            background-color: transparent;
            margin: 0 1rem;
            gap: 1rem;
        }

        .nav-tab {
            flex: 1;
            padding: 1rem;
            text-align: center;
            font-weight: 800;
            font-size: 1.1rem;
            cursor: pointer;
            background: white;
            border-radius: 20px;
            color: var(--text-muted);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
            border: 2px solid transparent;
        }

        .nav-tab.active {
            color: var(--primary);
            border: 2px solid var(--primary);
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(14, 165, 233, 0.2);
        }

        main {
            flex: 1;
            padding: 1.5rem;
            max-width: 800px;
            width: 100%;
            margin: 0 auto;
        }

        .view-section {
            display: none;
            animation: fadeIn 0.4s ease;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .view-section.active {
            display: block;
        }

        .card {
            background-color: var(--card-bg);
            border-radius: 24px;
            padding: 2rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05);
            border: 1px solid rgba(0,0,0,0.02);
        }

        .form-group {
            margin-bottom: 1.5rem;
        }

        label {
            display: block;
            margin-bottom: 0.6rem;
            font-size: 1.05rem;
            font-weight: 700;
            color: var(--text-dark);
        }

        select, input[type="text"] {
            width: 100%;
            padding: 1rem;
            background-color: #f8fafc;
            border: 2px solid var(--border);
            border-radius: 16px;
            color: var(--text-dark);
            font-size: 1.1rem;
            font-weight: 600;
            transition: border-color 0.2s;
        }
        
        select:focus, input[type="text"]:focus {
            outline: none;
            border-color: var(--primary);
        }

        .btn-capture {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.8rem;
            width: 100%;
            background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
            color: white;
            border: none;
            padding: 1.2rem;
            border-radius: 20px;
            font-size: 1.2rem;
            font-weight: 800;
            cursor: pointer;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 10px 15px -3px rgba(34, 197, 94, 0.3);
        }

        .btn-capture:active {
            transform: scale(0.95);
        }
        
        .btn-capture.blue {
            background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
            box-shadow: 0 10px 15px -3px rgba(14, 165, 233, 0.3);
        }

        .preview-box {
            margin-top: 1.5rem;
            text-align: center;
            display: none;
        }

        .preview-box img {
            max-width: 100%;
            max-height: 300px;
            border-radius: 16px;
            border: 4px solid var(--primary);
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        }

        .analysis-card {
            background: #f0fdf4;
            border: 2px solid #bbf7d0;
            border-radius: 20px;
            padding: 1.5rem;
            margin-top: 1.5rem;
            display: none;
        }

        .analysis-card.active {
            display: block;
        }

        .alert-socavon {
            background: #fef2f2;
            border: 2px solid #fecaca;
            color: #dc2626;
            padding: 1rem;
            border-radius: 16px;
            margin-top: 1rem;
            font-size: 1rem;
            font-weight: 800;
            display: flex;
            align-items: center;
            gap: 0.8rem;
        }

        .metric-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
            gap: 1rem;
            margin-bottom: 1.5rem;
        }

        .metric-card {
            background-color: white;
            border: 2px solid var(--border);
            border-radius: 16px;
            padding: 1.2rem;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        }

        .metric-val {
            font-size: 2rem;
            font-weight: 900;
            color: var(--primary);
            margin-top: 0.5rem;
        }

        .metric-val.danger {
            color: var(--danger);
        }

        #map {
            height: 400px;
            width: 100%;
            border-radius: 20px;
            border: 2px solid var(--border);
            z-index: 1;
            margin-bottom: 1.5rem;
        }

        .table-responsive {
            overflow-x: auto;
            background: white;
            border-radius: 20px;
            padding: 1rem;
            border: 1px solid var(--border);
        }

        table {
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 1rem;
        }

        th, td {
            padding: 1rem;
            border-bottom: 1px solid var(--border);
        }

        th {
            background-color: var(--bg-light);
            color: var(--text-dark);
            font-weight: 800;
            border-radius: 10px;
        }

        .badge-priority {
            padding: 0.4rem 0.8rem;
            border-radius: 9999px;
            font-weight: 800;
            font-size: 0.9rem;
        }

        .badge-high { background: #fee2e2; color: #ef4444; }
        .badge-med { background: #fef3c7; color: #f59e0b; }
        .badge-low { background: #d1fae5; color: #10b981; }

        .btn-dispatch {
            background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
            color: white;
            border: none;
            padding: 0.6rem 1rem;
            border-radius: 12px;
            font-size: 0.9rem;
            font-weight: 800;
            cursor: pointer;
            box-shadow: 0 4px 6px rgba(245, 158, 11, 0.3);
        }

        .btn-dispatch:active { transform: scale(0.95); }
"""

new_content = re.sub(r'<style>.*?</style>', f'<style>{new_css}</style>', content, flags=re.DOTALL)
with open('templates/index.html', 'w') as f:
    f.write(new_content)
