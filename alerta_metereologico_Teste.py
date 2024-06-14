import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import requests
from datetime import datetime

class AgroforecastApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Alertas Meteorológicos")
        self.root.geometry("350x600")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=1, fill='both')

        self.alerts_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.alerts_frame, text='Alertas Meteorológicos')

        self.create_alerts_tab()

    def create_alerts_tab(self):
        tk.Label(self.alerts_frame, text="Alertas Meteorológicos", font=("Helvetica", 16)).pack(pady=10)
        self.alerts_text = tk.Text(self.alerts_frame, wrap='word', width=40, height=20, font=('Helvetica', 12))
        self.alerts_text.pack(pady=10)

        self.fetch_alerts_button = ttk.Button(self.alerts_frame, text="Atualizar Alertas", command=self.fetch_alerts)
        self.fetch_alerts_button.pack(pady=10)

    def fetch_alerts(self):
        url = "http://api.openweathermap.org/data/2.5/alerts"  # Substitua pelo URL real
        headers = {'Content-Type': 'application/json'}
        data = {
            'appid': 'dfc79743c3c285e1152a9b0262a1bc5f'  # Adicione a chave da API, se necessário
        }

        try:
            response = requests.post(url, json=data, headers=headers)
            response_data = response.json()

            if response.status_code == 200:
                alert = response_data.get('alert', {})
                description = alert.get('description', [{}])[0]

                self.alerts_text.delete(1.0, tk.END)  # Limpa o texto anterior

                self.alerts_text.insert(tk.END, f"ID do Alerta: {alert.get('id', 'N/A')}\n")
                self.alerts_text.insert(tk.END, f"Tipo de Mensagem: {response_data.get('msg_type', 'N/A')}\n")
                self.alerts_text.insert(tk.END, f"Categorias: {', '.join(response_data.get('categories', []))}\n")
                self.alerts_text.insert(tk.END, f"Urgência: {response_data.get('urgency', 'N/A')}\n")
                self.alerts_text.insert(tk.END, f"Severidade: {response_data.get('severity', 'N/A')}\n")
                self.alerts_text.insert(tk.END, f"Certeza: {response_data.get('certainty', 'N/A')}\n")
                self.alerts_text.insert(tk.END, f"Início: {datetime.fromtimestamp(response_data.get('start', 0)).strftime('%d/%m/%Y %H:%M:%S')}\n")
                self.alerts_text.insert(tk.END, f"Fim: {datetime.fromtimestamp(response_data.get('end', 0)).strftime('%d/%m/%Y %H:%M:%S')}\n")
                self.alerts_text.insert(tk.END, f"Remetente: {response_data.get('sender', 'N/A')}\n")
                self.alerts_text.insert(tk.END, f"Língua: {description.get('language', 'N/A')}\n")
                self.alerts_text.insert(tk.END, f"Evento: {description.get('event', 'N/A')}\n")
                self.alerts_text.insert(tk.END, f"Título: {description.get('headline', 'N/A')}\n")
                self.alerts_text.insert(tk.END, f"Descrição: {description.get('description', 'N/A')}\n")
                self.alerts_text.insert(tk.END, f"Instruções: {description.get('instruction', 'N/A')}\n")
            else:
                messagebox.showerror("Erro", "Falha ao obter alertas meteorológicos.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao obter dados: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AgroforecastApp(root)
    root.mainloop()
