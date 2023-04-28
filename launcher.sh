#!/usr/bin/zsh


err_exit(){
  echo '[ERROR]'
  printf "%s " "Press enter to continue"
  read -r
  exit "$1"
}

# Get the option
r_key=false
update_symbols_key=false
str_param=""
pt="bsht.py"
printf "%s " "Params: "
while [ "$#" -gt 0 ]
do
   case "$1" in
   -f|--freeze)
      r_key=true
      printf "%s " " freeze;"
      ;;
   -u|--update-symbols)
      update_symbols_key=true
      printf "%s " " --update-symbols;"
      ;;
   --pt)
      shift
      pt="$1"
      printf "%s " " python file to start='$pt';"
      ;;
   --second-symbol)
      shift
      second_symbol="$1"
      str_param+="--second-symbol $second_symbol "
      printf "%s " " second-symbol='$second_symbol';"
      ;;
   --id)
      shift
      id="$1"
      str_param+="--id $id "
      printf "%s " " id=$id;"
      ;;
     --tests)
      shift
      tests="$1"
      str_param+="--tests $tests "
      printf "%s " " tests #'$tests';"
      ;;
     --force-url)
      force_url="--force-url"
      str_param+="$force_url "
      printf "%s " " $force_url';"
      ;;
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

echo "Venv activating:"
source ./venv/bin/activate || err_exit $?
echo "Venv activated successful"

if [ "$r_key" = true ]; then
    echo "pip freeze:"
    pip freeze
fi

# Start app
printf "\nStart app\n"
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