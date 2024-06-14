import tkinter as tk
from tkinter import Canvas, Entry, Label, messagebox, Text
from tkinter import ttk
import requests
from datetime import datetime
from tkintermapview import TkinterMapView
import logging
import re

# Configuração do logger para rastreamento e depuração
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AgroforecastApp:
    def __init__(self, root):
        """Inicializa a aplicação Agroforecast com a janela de login."""
        self.root = root
        self.root.title("Agroforecast Login")
        self.root.geometry("350x600")

        self.canvas = Canvas(self.root, width=350, height=600)
        self.canvas.pack()

        self.create_gradient('#0000FF', '#00FF00')  # Cria um fundo com gradiente de cor
        self.load_logo()  # Carrega o logo da aplicação
        self.create_entries()  # Cria campos de entrada para email e senha
        self.create_buttons()  # Cria botões de login e redes sociais
        self.create_links()  # Cria links para recuperação de senha e cadastro

        self.dark_mode = False  # Inicializa o modo escuro como desativado

    def create_gradient(self, color1, color2):
        """Cria um fundo com gradiente de cor."""
        width, height = 350, 600
        image = tk.PhotoImage(width=width, height=height)
        self.canvas.create_image(0, 0, image=image, anchor='nw')

        # Calcula a diferença entre as cores
        r1, g1, b1 = [x >> 8 for x in self.canvas.winfo_rgb(color1)]
        r2, g2, b2 = [x >> 8 for x in self.canvas.winfo_rgb(color2)]
        r_ratio = float(r2 - r1) / height
        g_ratio = float(g2 - g1) / height
        b_ratio = float(b2 - b1) / height

        # Cria o gradiente linha por linha
        for i in range(height):
            nr = int(r1 + (r_ratio * i))
            ng = int(g1 + (g_ratio * i))
            nb = int(b1 + (b_ratio * i))
            color = f'#{nr:02x}{ng:02x}{nb:02x}'
            image.put(color, to=(0, i, width, i + 1))

        self.gradient_image = image

    def load_logo(self):
        """Carrega e exibe o logo da aplicação."""
        try:
            original_logo = tk.PhotoImage(file="logo.png")
            scaled_logo = original_logo.subsample(2, 2)
            self.canvas.create_image(175, 100, image=scaled_logo, anchor='center')
            self.logo_image = scaled_logo
        except Exception as e:
            logging.error(f"Erro ao carregar o logo: {e}")
            messagebox.showerror("Erro", "Erro ao carregar o logo.")

    def create_entries(self):
        """Cria os campos de entrada para email e senha."""
        self.email_entry = Entry(self.root, width=30, font=('Helvetica', 12))
        self.email_entry.insert(0, 'Email')
        self.email_entry.bind("<FocusIn>", lambda event: self.clear_entry(event, self.email_entry, 'Email'))
        self.email_entry.bind("<FocusOut>", lambda event: self.add_placeholder(event, self.email_entry, 'Email'))
        self.canvas.create_window(175, 260, window=self.email_entry)

        self.password_entry = Entry(self.root, show='', width=30, font=('Helvetica', 12))
        self.password_entry.insert(0, 'Senha')
        self.password_entry.bind("<FocusIn>", lambda event: self.clear_entry(event, self.password_entry, 'Senha'))
        self.password_entry.bind("<FocusOut>", lambda event: self.add_placeholder(event, self.password_entry, 'Senha'))
        self.canvas.create_window(175, 310, window=self.password_entry)

    def create_buttons(self):
        """Cria os botões para login e login via redes sociais."""
        self.create_rounded_button(x=115, y=330, width=120, height=40, radius=20, text="ENTRAR", command=self.login)
        self.create_rounded_button(x=50, y=440, width=120, height=40, radius=20, text="Facebook", command=lambda: logging.info("Login Facebook"), fill_color="#3b5998")
        self.create_rounded_button(x=190, y=440, width=120, height=40, radius=20, text="Twitter", command=lambda: logging.info("Login Twitter"), fill_color="#1DA1F2")

    def create_links(self):
        """Cria links para recuperação de senha e cadastro."""
        forgot_password = Label(self.root, text="Esqueceu a senha?", fg="black", cursor="hand2")
        self.canvas.create_window(175, 390, window=forgot_password)

        signup_text = Label(self.root, text="Não tem conta? Inscrever-se", fg="blue", cursor="hand2")
        self.canvas.create_window(175, 500, window=signup_text)

    def create_rounded_button(self, x, y, width, height, radius, text, command, fill_color="#008000", text_color="white"):
        """Cria um botão arredondado."""
        def on_click(event):
            command()

        self.canvas.create_arc(x, y, x + 2 * radius, y + 2 * radius, start=90, extent=180, fill=fill_color, outline=fill_color)
        self.canvas.create_arc(x + width - 2 * radius, y, x + width, y + 2 * radius, start=0, extent=90, fill=fill_color, outline=fill_color)
        self.canvas.create_arc(x, y + height - 2 * radius, x + 2 * radius, y + height, start=180, extent=90, fill=fill_color, outline=fill_color)
        self.canvas.create_arc(x + width - 2 * radius, y + height - 2 * radius, x + width, y + height, start=270, extent=90, fill=fill_color, outline=fill_color)
        self.canvas.create_rectangle(x + radius, y, x + width - radius, y + height, fill=fill_color, outline=fill_color)
        self.canvas.create_rectangle(x, y + radius, x + width, y + height - radius, fill=fill_color, outline=fill_color)
        self.canvas.create_text(x + width / 2, y + height / 2, text=text, fill=text_color, font=('Helvetica', 12), anchor='center')

        button_id = self.canvas.create_rectangle(x, y, x + width, y + height, outline='', fill='', tags=("button",))
        self.canvas.tag_bind(button_id, "<ButtonPress-1>", on_click)

    def clear_entry(self, event, entry, default_text):
        """Limpa o texto de entrada padrão quando o campo recebe foco."""
        if entry.get() == default_text:
            entry.delete(0, tk.END)
            if entry == self.password_entry:
                entry.config(show='*')

    def add_placeholder(self, event, entry, default_text):
        """Adiciona texto de entrada padrão quando o campo perde foco."""
        if entry.get() == '':
            entry.insert(0, default_text)
            if entry == self.password_entry:
                entry.config(show='')

    def validate_email(self, email):
        """Valida o formato do email."""
        email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
        return re.match(email_regex, email) is not None

    def login(self):
        """Realiza o login do usuário e exibe as abas de previsão do tempo."""
        email = self.email_entry.get()
        password = self.password_entry.get()

        if email == '' or email == 'Email':
            messagebox.showerror("Erro", "Por favor, insira o email.")
            logging.warning("Tentativa de login sem email.")
        elif password == '' or password == 'Senha':
            messagebox.showerror("Erro", "Por favor, insira a senha.")
            logging.warning("Tentativa de login sem senha.")
        elif not self.validate_email(email):
            messagebox.showerror("Erro", "Por favor, insira um email válido.")
            logging.warning(f"Tentativa de login com email inválido: {email}")
        else:
            logging.info(f"Tentativa de login com Email: {email}")
            # Simulação de autenticação
            if email == "agroforecast@adm.com" and password == "adm":
                messagebox.showinfo("Sucesso", "Login bem-sucedido!")
                self.show_forecast_tabs()
            else:
                messagebox.showerror("Erro", "Email ou senha incorretos.")
                logging.warning("Tentativa de login com email ou senha incorretos.")

    def show_forecast_tabs(self):
        """Exibe as abas de previsão do tempo após o login."""
        self.canvas.pack_forget()

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=1, fill='both')

        self.location_frame = ttk.Frame(self.notebook)
        self.day_forecast_frame = ttk.Frame(self.notebook)
        self.hourly_forecast_frame = ttk.Frame(self.notebook)
        self.chatbot_frame = ttk.Frame(self.notebook)  # Nova aba para o chatbot

        self.notebook.add(self.location_frame, text='Localização')
        self.notebook.add(self.day_forecast_frame, text='Previsão do Dia')
        self.notebook.add(self.hourly_forecast_frame, text='Previsão Horária')
        self.notebook.add(self.chatbot_frame, text='Chatbot')  # Adiciona a nova aba ao notebook

        self.create_location_tab()
        self.create_day_forecast_tab()
        self.create_hourly_forecast_tab()
        self.create_chatbot_tab()  # Cria a nova aba do chatbot

    def create_location_tab(self):
        """Cria a aba de localização para entrada da cidade e exibição do mapa."""
        location_label = Label(self.location_frame, text="Localização", font=("Helvetica", 16))
        location_label.pack(pady=10)

        self.city_entry = Entry(self.location_frame, width=30, font=('Helvetica', 12))
        self.city_entry.insert(0, 'Digite a cidade')
        self.city_entry.bind("<FocusIn>", lambda event: self.clear_entry(event, self.city_entry, 'Digite a cidade'))
        self.city_entry.bind("<FocusOut>", lambda event: self.add_placeholder(event, self.city_entry, 'Digite a cidade'))
        self.city_entry.pack(pady=10)

        self.generate_button = ttk.Button(self.location_frame, text="Gerar", command=self.generate_forecast)
        self.generate_button.pack(pady=10)

        self.location_info = Label(self.location_frame, text="", font=("Helvetica", 12))
        self.location_info.pack()

        self.map_widget = TkinterMapView(self.location_frame, width=350, height=300, corner_radius=0)
        self.map_widget.pack(pady=10)

        # Adicionando o botão de modo escuro
        self.dark_mode_button = ttk.Button(self.location_frame, text="Modo Escuro", command=self.toggle_dark_mode)
        self.dark_mode_button.pack(pady=10)

    def generate_forecast(self):
        """Gera a previsão do tempo para a cidade fornecida."""
        self.city = self.city_entry.get()
        if self.city == '' or self.city == 'Digite a cidade':
            messagebox.showerror("Erro", "Por favor, insira o nome da cidade.")
        else:
            try:
                api_key = 'dfc79743c3c285e1152a9b0262a1bc5f'  # Chave da API OpenWeatherMap
                weather_response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={api_key}&lang=pt&units=metric')
                weather_response.raise_for_status()  # Verifica se a resposta foi bem-sucedida
                weather_data = weather_response.json()

                # Extraindo dados da resposta da API
                main = weather_data['main']
                weather = weather_data['weather'][0]
                wind = weather_data['wind']
                sys = weather_data['sys']
                clouds = weather_data['clouds']
                rain = weather_data.get('rain', {})

                # Processando dados extraídos
                max_temp = main['temp_max']
                min_temp = main['temp_min']
                precipitation = rain.get('1h', 0)  # Precipitação na última hora
                humidity = main['humidity']
                air_quality = 'N/A'  # Inicialmente como não disponível
                uv_index = 'N/A'  # Não disponível diretamente
                wind_speed = wind['speed']
                feels_like = main['feels_like']
                sunrise = datetime.fromtimestamp(sys['sunrise']).strftime('%H:%M')
                sunset = datetime.fromtimestamp(sys['sunset']).strftime('%H:%M')
                description = weather['description']
                visibility = weather_data['visibility']
                cloudiness = clouds['all']

                # Chamada à API de poluição do ar
                lat = weather_data['coord']['lat']
                lon = weather_data['coord']['lon']
                air_pollution_response = requests.get(f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}')
                air_pollution_response.raise_for_status()
                air_pollution_data = air_pollution_response.json()

                # Extraindo dados da resposta da API de poluição do ar
                air_quality_index = air_pollution_data['list'][0]['main']['aqi']
                pollutants = air_pollution_data['list'][0]['components']
                air_quality = self.get_air_quality_description(air_quality_index)

                # Componentes de poluição do ar
                co = pollutants.get('co', 'N/A')
                no = pollutants.get('no', 'N/A')
                no2 = pollutants.get('no2', 'N/A')
                o3 = pollutants.get('o3', 'N/A')
                so2 = pollutants.get('so2', 'N/A')
                pm2_5 = pollutants.get('pm2_5', 'N/A')
                pm10 = pollutants.get('pm10', 'N/A')
                nh3 = pollutants.get('nh3', 'N/A')

                # Atualize a aba de localização
                self.location_info.config(text=f"{self.city}\nMáx: {max_temp}°C  Mín: {min_temp}°C")

                # Atualize a aba de previsão do dia
                for widget in self.day_forecast_frame.winfo_children():
                    widget.destroy()
                Label(self.day_forecast_frame, text="Previsão do Dia", font=("Helvetica", 16)).pack(pady=10)
                Label(self.day_forecast_frame, text=f"Descrição: {description}").pack()
                Label(self.day_forecast_frame, text=f"Temperatura: {main['temp']}°C").pack()
                Label(self.day_forecast_frame, text=f"Màx: {max_temp}°C, Mín: {min_temp}°C").pack()
                Label(self.day_forecast_frame, text=f"Sensação térmica: {feels_like}°C").pack()
                Label(self.day_forecast_frame, text=f"Precipitação: {precipitation} mm").pack()
                Label(self.day_forecast_frame, text=f"Umidade: {humidity}%").pack()
                Label(self.day_forecast_frame, text=f"Qualidade do ar: {air_quality}").pack()
                Label(self.day_forecast_frame, text=f"CO: {co} μg/m³").pack()
                Label(self.day_forecast_frame, text=f"NO: {no} μg/m³").pack()
                Label(self.day_forecast_frame, text=f"NO2: {no2} μg/m³").pack()
                Label(self.day_forecast_frame, text=f"O3: {o3} μg/m³").pack()
                Label(self.day_forecast_frame, text=f"SO2: {so2} μg/m³").pack()
                Label(self.day_forecast_frame, text=f"PM2.5: {pm2_5} μg/m³").pack()
                Label(self.day_forecast_frame, text=f"PM10: {pm10} μg/m³").pack()
                Label(self.day_forecast_frame, text=f"NH3: {nh3} μg/m³").pack()
                Label(self.day_forecast_frame, text=f"Índice UV: {uv_index}").pack()
                Label(self.day_forecast_frame, text=f"Velocidade do vento: {wind_speed} m/s").pack()
                Label(self.day_forecast_frame, text=f"Visibilidade: {visibility} m").pack()
                Label(self.day_forecast_frame, text=f"Nebulosidade: {cloudiness}%").pack()
                Label(self.day_forecast_frame, text=f"Nascer do sol: {sunrise}").pack()
                Label(self.day_forecast_frame, text=f"Pôr do sol: {sunset}").pack()

                # Atualize o mapa interativo
                self.map_widget.set_position(lat, lon)
                self.map_widget.set_marker(lat, lon, text=self.city)
            except requests.exceptions.RequestException as e:
                logging.error(f"Erro na requisição de previsão do tempo: {e}")
                messagebox.showerror("Erro", "Erro ao obter dados de previsão do tempo.")
            except Exception as e:
                logging.error(f"Erro ao processar os dados de previsão do tempo: {e}")
                messagebox.showerror("Erro", f"Erro ao processar dados: {e}")

    def get_air_quality_description(self, index):
        """Retorna a descrição da qualidade do ar com base no índice fornecido."""
        if index == 1:
            return "Bom"
        elif index == 2:
            return "Justo"
        elif index == 3:
            return "Moderado"
        elif index == 4:
            return "Pobre"
        elif index == 5:
            return "Muito Pobre"
        else:
            return "Desconhecido"

    def create_day_forecast_tab(self):
        """Cria a aba de previsão do dia."""
        Label(self.day_forecast_frame, text="Previsão do Dia", font=("Helvetica", 16)).pack(pady=10)

    def create_hourly_forecast_tab(self):
        """Cria a aba de previsão horária."""
        Label(self.hourly_forecast_frame, text="Previsão Horária", font=("Helvetica", 16)).pack(pady=10)

        self.cnt_entry = Entry(self.hourly_forecast_frame, width=30, font=('Helvetica', 12))
        self.cnt_entry.insert(0, 'Número de previsões horárias')
        self.cnt_entry.bind("<FocusIn>", lambda event: self.clear_entry(event, self.cnt_entry, 'Número de previsões horárias'))
        self.cnt_entry.bind("<FocusOut>", lambda event: self.add_placeholder(event, self.cnt_entry, 'Número de previsões horárias'))
        self.cnt_entry.pack(pady=10)

        self.hourly_generate_button = ttk.Button(self.hourly_forecast_frame, text="Gerar", command=self.generate_hourly_forecast)
        self.hourly_generate_button.pack(pady=10)

        self.hourly_forecast_info = Text(self.hourly_forecast_frame, wrap='word', width=40, height=20, font=("Helvetica", 12), state='disabled')
        self.hourly_forecast_info.pack(pady=10)

    def generate_hourly_forecast(self):
        """Gera a previsão horária para a cidade fornecida."""
        cnt = self.cnt_entry.get()
        if not hasattr(self, 'city') or self.city == '' or self.city == 'Digite a cidade':
            messagebox.showerror("Erro", "Por favor, insira o nome da cidade na aba de Localização.")
        elif cnt == '' or cnt == 'Número de previsões horárias':
            messagebox.showerror("Erro", "Por favor, insira o número de previsões horárias.")
        else:
            try:
                cnt = int(cnt)  # Converte cnt para inteiro
                api_key = 'dfc79743c3c285e1152a9b0262a1bc5f'  # Chave da API OpenWeatherMap
                geocode_url = f"https://api.openweathermap.org/geo/1.0/direct?q={self.city}&appid={api_key}"
                geocode_requisicao = requests.get(geocode_url)
                geocode_requisicao.raise_for_status()
                geocode_dic = geocode_requisicao.json()

                if len(geocode_dic) > 0:
                    lat = geocode_dic[0]['lat']
                    lon = geocode_dic[0]['lon']
                    
                    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&cnt={cnt}&units=metric&lang=pt_br"
                    forecast_requisicao = requests.get(forecast_url)
                    forecast_requisicao.raise_for_status()
                    forecast_dic = forecast_requisicao.json()
                    
                    forecast_text = ""
                    for previsao in forecast_dic['list']:
                        dt = datetime.utcfromtimestamp(previsao['dt']).strftime('%Y-%m-%d %H:%M:%S')
                        temperatura = previsao['main']['temp']
                        feels_like = previsao['main']['feels_like']
                        temp_min = previsao['main']['temp_min']
                        temp_max = previsao['main']['temp_max']
                        pressure = previsao['main']['pressure']
                        humidity = previsao['main']['humidity']
                        descricao = previsao['weather'][0]['description']
                        clouds = previsao['clouds']['all']
                        wind_speed = previsao['wind']['speed']
                        wind_deg = previsao['wind']['deg']
                        rain = previsao.get('rain', {}).get('3h', 0)
                        visibility = previsao.get('visibility', 10000)
                        
                        forecast_text += (f"Data/Hora: {dt}\n"
                                          f"Temperatura: {temperatura}°C\n"
                                          f"Sensação térmica: {feels_like}°C\n"
                                          f"Temperatura mínima: {temp_min}°C\n"
                                          f"Temperatura máxima: {temp_max}°C\n"
                                          f"Pressão: {pressure} hPa\n"
                                          f"Umidade: {humidity}%\n"
                                          f"Descrição: {descricao}\n"
                                          f"Nuvens: {clouds}%\n"
                                          f"Velocidade do vento: {wind_speed} m/s\n"
                                          f"Direção do vento: {wind_deg}°\n"
                                          f"Chuva (últimas 3 horas): {rain} mm\n"
                                          f"Visibilidade: {visibility} metros\n"
                                          + "-" * 40 + "\n")

                    self.hourly_forecast_info.config(state='normal')
                    self.hourly_forecast_info.delete('1.0', tk.END)
                    self.hourly_forecast_info.insert(tk.END, forecast_text)
                    self.hourly_forecast_info.config(state='disabled')
                else:
                    messagebox.showerror("Erro", "Cidade não encontrada. Por favor, tente novamente.")
            except ValueError:
                logging.error("Erro ao converter número de previsões horárias para inteiro.")
                messagebox.showerror("Erro", "Por favor, insira um número válido para o número de previsões horárias.")
            except requests.exceptions.RequestException as e:
                logging.error(f"Erro na requisição de previsão horária: {e}")
                messagebox.showerror("Erro", "Erro ao obter dados de previsão horária.")
            except Exception as e:
                logging.error(f"Erro ao processar os dados de previsão horária: {e}")
                messagebox.showerror("Erro", f"Erro ao processar dados: {e}")

    def create_chatbot_tab(self):
        """Cria a aba do chatbot para interação com os usuários."""
        Label(self.chatbot_frame, text="Chatbot para Agricultores", font=("Helvetica", 16)).pack(pady=10)

        self.chat_input = Entry(self.chatbot_frame, width=50, font=('Helvetica', 12))
        self.chat_input.insert(0, 'Digite sua pergunta...')
        self.chat_input.bind("<FocusIn>", lambda event: self.clear_entry(event, self.chat_input, 'Digite sua pergunta...'))
        self.chat_input.bind("<FocusOut>", lambda event: self.add_placeholder(event, self.chat_input, 'Digite sua pergunta...'))
        self.chat_input.bind("<Return>", lambda event: self.process_question())
        self.chat_input.pack(pady=10)

        self.chat_output = Text(self.chatbot_frame, wrap='word', width=40, height=15, font=("Helvetica", 12), state='disabled', bg="#f0f0f0")
        self.chat_output.pack(pady=10)

        self.send_button = ttk.Button(self.chatbot_frame, text="Enviar", command=self.process_question)
        self.send_button.pack(pady=10)

    def process_question(self):
        """Processa a pergunta do usuário e retorna a resposta."""
        question = self.chat_input.get()
        if question == '' or question == 'Digite sua pergunta...':
            messagebox.showerror("Erro", "Por favor, insira uma pergunta.")
        else:
            answer = self.get_chatbot_response(question)
            self.chat_output.config(state='normal')
            self.chat_output.insert(tk.END, f"Pergunta: {question}\nResposta: {answer}\n{'-' * 40}\n")
            self.chat_output.config(state='disabled')

    def get_chatbot_response(self, question):
        """Retorna uma resposta predefinida com base na pergunta fornecida."""
        predefined_qa = {
            "Qual a previsão de chuva para hoje?": "A previsão indica chuva leve no final da tarde, acumulando cerca de 5 mm.",
            "Como estará a umidade do solo amanhã?": "A umidade do solo estará alta devido às chuvas previstas para esta noite.",
            "Qual a melhor hora para irrigar as plantações amanhã?": "A melhor hora para irrigar será pela manhã, antes das 10h, para evitar a evaporação excessiva.",
            "Haverá geada nos próximos dias?": "Não há previsão de geada nos próximos cinco dias.",
            "Qual a temperatura mínima esperada para esta semana?": "A temperatura mínima esperada é de 12°C na quarta-feira.",
            "Qual a previsão de ventos fortes para hoje?": "Haverá ventos fortes à tarde, com rajadas de até 30 km/h.",
            "Quando será o próximo período de seca?": "Um período de seca é esperado para começar em duas semanas, durando cerca de cinco dias.",
            "Qual a previsão de temperatura para o próximo fim de semana?": "A temperatura deve variar entre 18°C e 25°C no próximo fim de semana.",
            "Haverá tempestades amanhã?": "Sim, tempestades são esperadas para amanhã à noite, com risco de granizo.",
            "Qual o índice de radiação UV para hoje?": "O índice de radiação UV será alto hoje, alcançando um valor de 8 ao meio-dia.",
            "Como estará a visibilidade para pulverização de defensivos amanhã?": "A visibilidade estará boa pela manhã, com condições adequadas para pulverização.",
            "Quando será o próximo período de clima seco?": "O próximo período de clima seco começará daqui a três dias e durará cerca de uma semana.",
            "Haverá risco de inundações esta semana?": "Não há risco de inundações previsto para esta semana.",
            "Qual a previsão de temperatura máxima para hoje?": "A temperatura máxima esperada para hoje é de 28°C.",
            "Qual a quantidade esperada de chuva para os próximos três dias?": "A previsão é de 15 mm de chuva acumulada nos próximos três dias.",
            "Haverá mudanças bruscas de temperatura nos próximos dias?": "Sim, haverá uma queda de temperatura de cerca de 10°C na próxima sexta-feira.",
            "Qual a previsão de umidade relativa do ar para amanhã?": "A umidade relativa do ar estará em torno de 70% pela manhã.",
            "Qual o melhor dia para colher trigo nesta semana?": "Sexta-feira será o melhor dia, com previsão de tempo seco e temperaturas amenas.",
            "Haverá neblina nos próximos dias?": "Sim, neblina densa é esperada na madrugada de quinta-feira.",
            "Qual a previsão de raios UV para o fim de semana?": "Os índices de UV estarão moderados no fim de semana, variando entre 4 e 6.",
            "Quando é o melhor horário para aplicar fertilizantes?": "O melhor horário para aplicação será no início da manhã, antes das 9h.",
            "Haverá condições favoráveis para a ocorrência de pragas esta semana?": "Sim, o clima úmido previsto pode favorecer a ocorrência de pragas.",
            "Qual a previsão de ventos para os próximos três dias?": "Ventos moderados, com velocidade média de 15 km/h, são esperados nos próximos três dias.",
            "Haverá nevasca nos próximos dias?": "Não há previsão de nevasca para os próximos dias.",
            "Qual a previsão de temperatura durante a noite para esta semana?": "As temperaturas noturnas variarão entre 15°C e 20°C durante esta semana."
        }
        return predefined_qa.get(question, f"Desculpe, não tenho uma resposta para '{question}'.")

    def toggle_dark_mode(self):
        """Alterna entre os modos claro e escuro."""
        if hasattr(self, 'dark_mode') and self.dark_mode:
            # Modo claro
            self.apply_light_mode()
            self.dark_mode = False
        else:
            # Modo escuro
            self.apply_dark_mode()
            self.dark_mode = True

    def apply_dark_mode(self):
        """Aplica o modo escuro à interface."""
        # Alterar cores dos widgets para o modo escuro
        style = ttk.Style()
        style.configure('TFrame', background='#333333')
        style.configure('TLabel', background='#333333', foreground='#FFFFFF')
        style.configure('TEntry', fieldbackground='#333333', foreground='#FFFFFF', insertcolor='#FFFFFF')
        style.configure('TButton', background='#333333', foreground='#FFFFFF')

        self.root.configure(bg="#333333")
        self.location_frame.configure(style='TFrame')
        self.day_forecast_frame.configure(style='TFrame')
        self.hourly_forecast_frame.configure(style='TFrame')
        self.chatbot_frame.configure(style='TFrame')

        # Alterar cores dos rótulos e entradas
        for widget in self.location_frame.winfo_children():
            if isinstance(widget, Label):
                widget.configure(bg="#333333", fg="#FFFFFF")
            elif isinstance(widget, Entry):
                widget.configure(bg="#333333", fg="#FFFFFF", insertbackground="#FFFFFF")

        for widget in self.day_forecast_frame.winfo_children():
            if isinstance(widget, Label):
                widget.configure(bg="#333333", fg="#FFFFFF")
            elif isinstance(widget, Entry):
                widget.configure(bg="#333333", fg="#FFFFFF", insertbackground="#FFFFFF")

        for widget in self.hourly_forecast_frame.winfo_children():
            if isinstance(widget, Label):
                widget.configure(bg="#333333", fg="#FFFFFF")
            elif isinstance(widget, Entry):
                widget.configure(bg="#333333", fg="#FFFFFF", insertbackground="#FFFFFF")
            elif isinstance(widget, Text):
                widget.configure(bg="#333333", fg="#FFFFFF", insertbackground="#FFFFFF")

        for widget in self.chatbot_frame.winfo_children():
            if isinstance(widget, Label):
                widget.configure(bg="#333333", fg="#FFFFFF")
            elif isinstance(widget, Entry):
                widget.configure(bg="#333333", fg="#FFFFFF", insertbackground="#FFFFFF")
            elif isinstance(widget, Text):
                widget.configure(bg="#333333", fg="#FFFFFF", insertbackground="#FFFFFF")

    def apply_light_mode(self):
        """Aplica o modo claro à interface."""
        # Reverter para as cores do modo claro
        style = ttk.Style()
        style.configure('TFrame', background='#FFFFFF')
        style.configure('TLabel', background='#FFFFFF', foreground='#000000')
        style.configure('TEntry', fieldbackground='#FFFFFF', foreground='#000000', insertcolor='#000000')
        style.configure('TButton', background='#FFFFFF', foreground='#000000')

        self.root.configure(bg="#FFFFFF")
        self.location_frame.configure(style='TFrame')
        self.day_forecast_frame.configure(style='TFrame')
        self.hourly_forecast_frame.configure(style='TFrame')
        self.chatbot_frame.configure(style='TFrame')

        # Reverter cores dos rótulos e entradas
        for widget in self.location_frame.winfo_children():
            if isinstance(widget, Label):
                widget.configure(bg="#FFFFFF", fg="#000000")
            elif isinstance(widget, Entry):
                widget.configure(bg="#FFFFFF", fg="#000000", insertbackground="#000000")

        for widget in self.day_forecast_frame.winfo_children():
            if isinstance(widget, Label):
                widget.configure(bg="#FFFFFF", fg="#000000")
            elif isinstance(widget, Entry):
                widget.configure(bg="#FFFFFF", fg="#000000", insertbackground="#000000")

        for widget in self.hourly_forecast_frame.winfo_children():
            if isinstance(widget, Label):
                widget.configure(bg="#FFFFFF", fg="#000000")
            elif isinstance(widget, Entry):
                widget.configure(bg="#FFFFFF", fg="#000000", insertbackground="#000000")
            elif isinstance(widget, Text):
                widget.configure(bg="#FFFFFF", fg="#000000", insertbackground="#000000")

        for widget in self.chatbot_frame.winfo_children():
            if isinstance(widget, Label):
                widget.configure(bg="#FFFFFF", fg="#000000")
            elif isinstance(widget, Entry):
                widget.configure(bg="#FFFFFF", fg="#000000", insertbackground="#000000")
            elif isinstance(widget, Text):
                widget.configure(bg="#FFFFFF", fg="#000000", insertbackground="#000000")

class SplashScreen:
    def __init__(self, splash_root):
        """Inicializa a tela de splash."""
        self.splash_root = splash_root
        self.splash_root.title("Agroforecast")

        splash_canvas = Canvas(self.splash_root, width=350, height=600, bg='#0000FF')
        splash_canvas.pack()

        splash_logo = tk.PhotoImage(file="logo.png")
        scaled_splash_logo = splash_logo.subsample(2, 2)
        splash_canvas.create_image(175, 300, image=scaled_splash_logo, anchor='center')
        self.splash_logo_image = scaled_splash_logo

        self.splash_root.after(3000, self.show_login)

    def show_login(self):
        """Fecha a tela de splash e exibe a tela de login."""
        self.splash_root.destroy()
        root = tk.Tk()
        root.geometry("350x600")
        app = AgroforecastApp(root)
        root.mainloop()

if __name__ == "__main__":
    splash_root = tk.Tk()
    SplashScreen(splash_root)
    splash_root.mainloop()
