
# [Source File]
#   1:00
#       Subtitle 1
#   1:30
#       Subtitle 2
#   1:60
#       Subtitle 3


# [Target File]
#   00:01:00 --> 00:01:30
#       Subtitle 1
#   00:01:30 -->  00:01:60
#       Subtitle 2
#   00:01:60 -->  00:01:90
#       Subtitle 3



#__________________________________________________________________________________________

def printf(str, printable=False):
#{
    if printable:
        print(str)
#}

#__________________________________________________________________________________________

def reformatTime(times):
#{
    paramIsString=False;
    formated_times = [];

    if isinstance(times, int):
        str_time = str(times)        
        if len( str_time ) == 1:
            return "0" + str_time        
        return str_time

    if isinstance(times, str):
        paramIsString=True;
        times = [times];

    for time in times:
    #{
        formated_time  = ""        

        if time.count(":") == 1:
        #{
            MS = time.split(":");
  
            MM = MS[0]
            SS = MS[1]

            #Hour
            HH = "00"

            #Minute
            if len(MM) == 1:
                MM = "0" + MM;

            #Second
            if len(SS) == 1:
                SS = "0" + SS;

            formated_time = HH + ":" + MM + ":" + SS;

        #}

        elif time.count(":") == 2:
        #{    
            HMS = time.split(":");

            HH = HMS[0] 
            MM = HMS[1]
            SS = HMS[2]

            #Hour
            if len(HH) == 1:
                HH = "0" + HH;

            #Minute
            if len(MM) == 1:
                MM = "0" + MM;

            #Second
            if len(SS) == 1:
                SS = "0" + SS;

            formated_time = HH + ":" + MM + ":"  + SS;       
        #}


        formated_times.append(formated_time)
    #}

    printf(formated_times);

    if paramIsString:
        return formated_times[0]

    return formated_times;
#}

#__________________________________________________________________________________________

def readFile(file_path):
#{
    lines = [];

    with open(file_path, 'r') as file:
    #{
        for line in file:
        #{
            lines.append(line.strip())
        #}
    #}

    printf(lines);
    return lines;
#}

#__________________________________________________________________________________________

def detect_times_from_file(file_path):
#{

    lines = readFile(file_path)
    times = [];

    for line in lines:
    #{
        index = line.find(":")

        if index != -1:
            times.append(line)
    #}    

    printf(times);
    return times;
#}

#__________________________________________________________________________________________

def add_time_strings(time1_str, time2_str):
#{
    HH=""
    MM=""
    SS=""

    if isinstance(time1_str, str) and isinstance(time2_str, str) :
    #{
        if time1_str.count(":")==2 and time2_str.count(":")==2:
        #{
            HMS1 = time1_str.split(":")
            HMS2 = time2_str.split(":")

            SS  =   (( int(HMS1[2]) + int(HMS2[2]) ) % 60 )
            MM_ =   (( int(HMS1[1]) + int(HMS2[1]) ) + ( (int(HMS1[2]) + int(HMS2[2])) // 60 ))
            MM  =   MM_ % 60
            HH  =   (( int(HMS1[0]) + int(HMS2[0]) ) + ( MM_ // 60 )) 
        #}
    #}

    elif isinstance(time1_str, str):
    #{
        if time1_str.count(":")== 2 and time2_str > 0:
        #{
            HMS1 = time1_str.split(":")

            SS = int(HMS1[2]) + (time2_str % 60)
            MM = int(HMS1[1]) + (time2_str % 3600 // 60)
            HH = int(HMS1[0]) + (time2_str // 3600) 
        #}
    #}

    return str(HH) + ":" + str(MM) + ":" + str(SS)
#}

#__________________________________________________________________________________________

SHAPE_REPEAT  = 25
BORDER_A      = "-^" * SHAPE_REPEAT + "\n"
BORDER_P      = "^-" * SHAPE_REPEAT + "\n"
BANNER_TITLE  = "{0}This Subtitles Reformated By: Aminofory\n{0}Aminofory@gmail.com\n"
SEPARATOR     = "\n"
BANNER_REPEAT = 10 # number of seconds that the banner will display

BANNER = [ 
              BORDER_A\
            + BANNER_TITLE\
            + BORDER_A\
            + SEPARATOR
            ,
              BORDER_P\
            + BANNER_TITLE\
            + BORDER_P\
            + SEPARATOR
         ]


def writeFile_formatedTime( file_path, exported_fileName, subtitle_disappear_after_sec=5 ):
#{
    times = detect_times_from_file(file_path)
    formated_times = reformatTime(times);

    lines = readFile(file_path);    

    time_flag = 0;

    with open(exported_fileName, 'w') as file:
    #{
        for index in range(0, len(lines)):      
        #{
            if lines[index].find(":") != -1:
            #{
                newLine = ""                

                if time_flag == 0:
                #{
                    switch =0;
                    STR = END = 0;

                    banner_counter = 0;

                    for step in range(1, BANNER_REPEAT+1, 1):
                    #{                        
                        STR = END;
                        END = step;

                        newLine += str(banner_counter+1) + "\n"\
                                +"00:00:" + reformatTime(STR) + " --> 00:00:" + reformatTime(END)  + "\n"\
                                + BANNER[switch].format("");
                        
                        switch = 0 if switch==1 else 1;

                        banner_counter += 1;
                    #}
                #}

                counter = time_flag + banner_counter + 1

                #END == NEXT
                if subtitle_disappear_after_sec == 0:
                    STR = formated_times[time_flag];

                    if time_flag+1 < len(formated_times):
                        END = formated_times[time_flag+1];
                    else:
                        END = reformatTime( add_time_strings( formated_times[time_flag], (writeFile_formatedTime.__defaults__)[0] ));

                #END == START + SECONDS
                elif subtitle_disappear_after_sec > 0:
                    STR = formated_times[time_flag];
                    END = reformatTime( add_time_strings( formated_times[time_flag], subtitle_disappear_after_sec ) );
                

                newLine += "\n" + str(counter) + "\n" + STR + " --> " + END;
            
                lines[index] = newLine;

                time_flag +=1;        
            #}

            file.write(lines[index] + "\n")
        #}
    #}
        
    print("\nSRT File Generated [Successfully]")    
    print("SRT File Generated By: Aminofory@gmail.com")
    print("Enjoy ;)")
#}

#__________________________________________________________________________________________

#***************
# Entry Point:
#***************

file_path = input("Please Enter The Subtitles File Path That You Want To Reformat:\n")
#Enter the subtitles file path that you want to reformat to VLC format
#file_path = "D:/Media/Videos/Noah 2014/Noah.srt";
#file_path = "D:\\Media\\Videos\\Noah 2014\\Noah.srt";
#file_path = "C:\\Users\\Administrator\\Downloads\\Video\\Adele-Hello.txt";

#Export SRT or txt file that support for VLC player
#subtitle_disappear_after_sec==0  , END == NEXT
#subtitle_disappear_after_sec > 0 , END == START + subtitle_disappear_after_sec
writeFile_formatedTime(file_path= file_path, 
                       exported_fileName= "C:/My_VLC_Subtitle.srt",
                       subtitle_disappear_after_sec= 5);

#__________________________________________________________________________________________
