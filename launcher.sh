#!/bin/bash


err_exit(){
  echo '[ERROR]'
  printf "%s " "Press enter to continue"
  read -r
  exit "$1"
}

# Get the option
r_key=false
update_key=false
install_key=false
str_param=""
pt="app.py"

printf "%s " "Params: "
while [ "$#" -gt 0 ]
do
   case "$1" in
   install)
      install_key=true
      ;;

   -f|--freeze)
      r_key=true
      printf "%s " " freeze;"
      ;;

#   -u|--update)
#      update_key=true
#      printf "%s " " --update;"
#      ;;

   --pt)
      shift
      pt="$1"
      printf "%s " " python file to start='$pt';"
      ;;

   --start-date)
      shift
      start_date="$1"
      str_param+="--start-date $start_date "
      printf "%s " " start-date='$start_date';"
      ;;

   --end-date)
      shift
      end_date="$1"
      str_param+="--end-date $end_date "
      printf "%s " " end-date='$end_date';"
      ;;

#     --tests)
#      shift
#      tests="$1"
#      str_param+="--tests $tests "
#      printf "%s " " tests #'$tests';"
#      ;;
#
#
     -h|--help)
      help="--help"
      str_param+="$help "
      printf "%s " " $help';"
      ;;

   -*)
      echo "Invalid option '$1'. Use -h or --help to see the valid options" >&2
      return 1
      ;;

   *)
      echo "Invalid option '$1'. Use -h or --help to see the valid options" >&2
      return 1
   ;;
   esac
   shift
done
echo

echo "start_dir: $(pwd)"
start_dir=$(pwd)

echo "base_dir: $(dirname "$0")"
base_dir=$(dirname "$0")
if [ "$base_dir" != "." ]; then
  echo "Changing directory to: $base_dir"
  cd "$base_dir" || err_exit $?
  echo "pwd: $(pwd)"
fi

# Installation of utils and requirements
if [ "$install_key" = true ]; then
    printf "\n\033[93m%s\033[0m\n" "Installation process"

    printf "\n\033[93m%s\033[0m\n" "python3 installation"
    sudo apt install python3

    printf "\n\033[93m%s\033[0m\n" "MongoDB installation"
    sudo apt-get install gnupg
    echo "deb [ signed-by=/usr/share/keyrings/mongodb-server-6.0.gpg] http://repo.mongodb.org/apt/debian bullseye/mongodb-org/6.0 main" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
    sudo apt-get update
    sudo apt-get install -y mongodb-org
    sudo systemctl start mongod

    printf "\n\033[93m%s\033[0m\n" "Tesseract OCR installation"
    sudo apt-get install tesseract-ocr

    printf "\n\033[93m%s\033[0m\n" "Virtual environment installation"
    python3 -m pip install --user --upgrade pip
    python3 -m pip install --user virtualenv
    source ./venv/bin/activate || err_exit $?

    printf "\n\033[93m%s\033[0m\n" "Requirements installation"
    pip install -r requirements.txt

    printf "\n\033[93m%s\033[0m\n" "Installed successfully"
    printf "%s " "Press enter to continue"
    read -r
    exit
fi

echo "Venv activating:"
source ./venv/bin/activate || err_exit $?
echo "Venv activated successful"

if [ "$r_key" = true ]; then
    echo "pip freeze:"
    pip freeze
fi

# Start MongoDB
echo "Starting MongoDB (It may requests permission)"
sudo systemctl start mongod

# Start app
printf "\n\033[93m%s\033[0m\n" "Start app"
printf "%s\n" "python $pt $str_param > "
echo "$str_param" | xargs python "$pt"
printf "\n%s\n\n" "< python $pt $str_param"

# Starting bot with
# printf "\n%s\n" "Starting bot with args: $str_param "
# printf "python ./bot_logic.py > \n"
# while true ; do echo "$str_param" | xargs python ./bot_logic.py || sleep 5; done
# printf "< python ./bot_logic.py\n\n"

echo "Changing directory to: $start_dir"
cd "$start_dir" || err_exit $?
echo "pwd: $(pwd)"

deactivate