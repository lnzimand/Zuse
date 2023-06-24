using System;
using System.Collections.Generic;
using System.Data.Odbc;
using System.Net.WebSockets;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;
using Newtonsoft.Json;
using System.Data;

namespace ServiceApplication
{
    public partial class Service : Form
    {
        private ClientWebSocket webSocket;
        private OdbcConnection connection;
        private readonly string query = @"
            SELECT
                U.user_id, U.name, U.username, U.email,
                U.phone, U.website, A.street, A.suite,
                A.city, A.zipcode, G.lat, G.lng,
                C.name AS company_name, C.catchphrase, C.bs
            FROM
                [User] U
                INNER JOIN Address A ON U.address_id = A.address_id
                INNER JOIN Geo G ON A.geo_id = G.geo_id
                INNER JOIN Company C ON U.company_id = C.company_id
            WHERE U.user_id = ?";

        public Service()
        {
            InitializeComponent();
            InitializeWebSocket();
            InitializeDatabaseConnection();
            StartService();
        }

        private void InitializeWebSocket()
        {
            webSocket = new ClientWebSocket();
        }

        private void InitializeDatabaseConnection()
        {
            var connectionString = "Driver={SQL Server};Server=DESKTOP-STVGQ9Q;Database=project_csharp;Uid=odbc_user;Pwd=password;";
            connection = new OdbcConnection(connectionString);
        }

        private async void StartService()
        {
            try
            {
                await webSocket.ConnectAsync(new Uri("ws://localhost:8000/ws-advanced"), CancellationToken.None);
                await StartDatabaseQueryAndSendData(new CancellationTokenSource().Token);
            }
            catch (WebSocketException ex)
            {
                if (ex.InnerException is SocketException socketException)
                {
                    if (socketException.SocketErrorCode == SocketError.ConnectionAborted)
                    {
                        Console.WriteLine("WebSocket connection was prematurely closed by the host machine");
                    }
                }
                else
                {
                    Console.WriteLine($"WebSocket exception occurred: {ex.Message}");
                }
            }
        }

        private async Task StartDatabaseQueryAndSendData(CancellationToken cancellationToken)
        {
            try
            {
                var command = new OdbcCommand(query, connection);
                var buffer = new byte[1024 * 4];

                while (!cancellationToken.IsCancellationRequested && webSocket.State == WebSocketState.Open)
                {
                    try
                    {
                        int placeHolderId = new Random().Next(1, 100);
                        List<object> results = new List<object>();

                        await connection.OpenAsync(cancellationToken);
                        command.Parameters.AddWithValue("@Id", placeHolderId);
                        var reader = await command.ExecuteReaderAsync(CommandBehavior.CloseConnection, cancellationToken);

                        while (reader.Read())
                        {
                            var jsonData = new
                            {
                                action = "create_user",
                                user = new
                                {
                                    name = reader["name"].ToString(),
                                    username = reader["username"].ToString(),
                                    email = reader["email"].ToString(),
                                    phone = reader["phone"].ToString(),
                                    website = reader["website"].ToString(),
                                    address = new
                                    {
                                        street = reader["street"].ToString(),
                                        suite = reader["suite"].ToString(),
                                        city = reader["city"].ToString(),
                                        zipcode = reader["zipcode"].ToString(),
                                        geo = new
                                        {
                                            lat = reader["lat"].ToString(),
                                            lng = reader["lng"].ToString()
                                        }
                                    },
                                    company = new
                                    {
                                        name = reader["company_name"].ToString(),
                                        catchphrase = reader["catchphrase"].ToString(),
                                        bs = reader["bs"].ToString()
                                    }
                                }
                            };
                            results.Add(jsonData);
                        }

                        reader.Close();

                        if (results.Count > 0)
                        {
                            string json = JsonConvert.SerializeObject(results[0], Formatting.Indented);
                            byte[] jsonBytes = Encoding.UTF8.GetBytes(json);
                            ArraySegment<byte> segment = new ArraySegment<byte>(jsonBytes);

                            await webSocket.SendAsync(segment, WebSocketMessageType.Text, true, cancellationToken);

                            WebSocketReceiveResult result = await webSocket.ReceiveAsync(new ArraySegment<byte>(buffer), cancellationToken);
                            Console.WriteLine(Encoding.UTF8.GetString(buffer, 0, result.Count));
                        }

                        await Task.Delay(5000, cancellationToken);
                    }
                    catch (WebSocketException ex)
                    {
                        Console.WriteLine($"WebSocket exception occurred: {ex.Message}");
                        break;
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.ToString());
            }
            finally
            {
                if (connection.State != ConnectionState.Closed)
                    connection.Close();
            }
        }


        private void exitToolStripMenuItem_Click(object sender, EventArgs e)
        {
            webSocket.CloseAsync(WebSocketCloseStatus.NormalClosure, "Service stopped", CancellationToken.None).Wait();
            webSocket.Dispose();
            connection.Dispose();
            Application.Exit();
        }
    }
}
