# $1 is path of midiconverter
# $2 is path of folder with midi files
# $3 is path of outputfolder for the xmlfiles

#./miditoxml.sh "/Applications/MuseScore\ 2.app/Contents/MacOS/mscore" "./songs-midi" "./songs-xml"


for instance in "$2"/* # Loop over every instance file in the instances folder
        do

            y=${instance%.midi} # get part before .txt
            filename=${y##*/} # Only keep filename (remove the path)
            output="$3/$filename.xml"
            echo "$1 -I $instance -o $output"
            eval "$1 -I $instance -o $output"

        done