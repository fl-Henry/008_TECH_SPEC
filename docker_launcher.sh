#!/bin/bash

# Get the option
str_param=""

printf "%s " "Params: "
while [ "$#" -gt 0 ]
do
   case "$1" in

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

docker run -d --network mongo --network-alias db -v $(pwd)/db_data:/data/db --name mongodb_img mongo:4.2.24 >/dev/null

# Start app
printf "\n\033[93m%s\033[0m\n" "Start app"
docker run -it --rm --network mongo tech_spec_local python3 app.py $str_param

docker stop mongodb_img >/dev/null

docker rm -f $(docker ps -a -q) >/dev/null

echo "Changing directory to: $start_dir"
cd "$start_dir" || err_exit $?
echo "pwd: $(pwd)"