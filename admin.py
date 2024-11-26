from flask import Flask, jsonify
from flask_cors import CORS
from mcstatus import JavaServer
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Povolí CORS
connected_players = {}

server_address = "192.168.0.126"

@app.route("/api/players", methods=["GET"])
def get_player_count():
    try:
        server = JavaServer.lookup(server_address)
        status = server.status()
        current_players = [player.name for player in status.players.sample or []]
        now = datetime.now()
        for player in current_players:
            if player not in connected_players:
                connected_players[player] = now
        for player in list(connected_players.keys()):
            if player not in current_players:
                del connected_players[player]
        players_with_time = []
        for player, connect_time in connected_players.items():
            elapsed_time = (now - connect_time).total_seconds()
            players_with_time.append({
                "name": player,
                "connected_time": elapsed_time
            })
        
        return jsonify(
            {"online_players": status.players.online,
             "players": status.players.sample,
             "ping": status.latency,
             "players_with_time": players_with_time})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    context = ('cert.pem', 'key.pem')  # Cesta k vašim SSL certifikátům
    app.run(host="0.0.0.0", port=5281, ssl_context=context)
