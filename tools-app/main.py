from tools_app.app import app

if __name__ == "__main__":
    print("Starting tools application")
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)