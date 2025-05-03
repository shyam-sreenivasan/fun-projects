## Export environment variables
export UPLOAD_FOLDER="some path"
export MEDIA_BACKUP_PATH="some path"

## Switch to working directory
cd tools-app

## create virutal env
python3 -m venv py3

## Switch to virutal environment
source py3/bin/activate

## Install dependencies
pip install -r requirements.txt

## Run app
python main.py

--------------------------------------------------------------------
## optional shortcut to setup in .bashrc file
export TOOLS_APP="full path to tools app"

mytools() {
    case "$1" in
        start)
            cd $TOOLS_APP && nohup py3/bin/python main.py 2>&1 &
            ;;
        stop)
            pkill -f "py3/bin/python main.py"
            ;;
        restart)
            $0 stop
            sleep 1
            $0 start
            ;;
        *)
            echo "Usage: mytools {start|stop|restart}"
            return 1
            ;;
    esac
}


