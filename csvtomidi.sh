# $1 is path of csvconverter
# $2 is path of folder with csv files
# $3 is path of outputfolder for the midefiles
# $4 extension


for instance in "$2"/* # Loop over every instance file in the instances folder
        do

            y=${instance%.csv} # get part before .txt
            filename=${y##*/} # Only keep filename (remove the path)
            output="$3/$filename.midi"
            echo "$1 $instance $output"
            eval "$1 $instance $output"
           
            # first=$(echo ${filename:3:$length-4}  | awk '{print toupper($0)}')
            # second=${filename:$length-1:1}
            # echo "$first.$second $cost" >> "$3/$configuration.txt"
        done