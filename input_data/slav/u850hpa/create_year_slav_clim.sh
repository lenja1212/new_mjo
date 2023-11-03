#!/bin/bash

fntmp_list=""
dir_temp="./temp/"
ensmean_year="./erfclim.all-ensmean-u850hpa.nc"
month_30=("4" "6" "9" "11")
month_31=("1" "3" "5" "7" "8" "10" "12")
start_hour="00:00:00"

#======================================
function generate_tmp_nc_names() {
    while [ $# -gt 0 ]; do
        local tmp_name=$1
        local tmp_file=$dir_temp"temp"${RANDOM}${RANDOM}$nc
        fntmp_list=$fntmp_list" "$tmp_file
        if [[ "$tmp_name" ]]; then
            eval $tmp_name="'$tmp_file'"
        else
            echo "$fn"
        fi
        shift
    done
}

#======================================
function generate_dir_out() {
    for dir in $dir_temp; do
        if [ ! -d $dir ]; then
            echo "creating: "$dir
            mkdir -p $dir
        fi
    done
}

#======================================
function delete_tmp_files() {
	echo "remove fntmp_list"
    for fn in $fntmp_list; do
        if [ -e $fn ]; then
            # echo "remove $fn"
            rm $fn
        fi
    done    
}

#======================================

generate_dir_out dir_temp
generate_tmp_nc_names tmp_merge_in

let processed_members=0
start_date=$(date '+%Y%m%d ' --date="1991-01-02 00:00:00 UTC")


for f in `ls *.ensmean-*`; do
	generate_tmp_nc_names tmp1 tmp2 tmp_ax1 tmp_merge_out
	echo $f
	date=$(echo $f |  grep -oP '(?<=[.])\w+(?=[.])')
	month=${date:0:2}
	day=${date:2:4}
	echo "day:"$day
	echo "month:"$month

	cdo -settaxis,1991-01-02,$start_hour,1day $f $tmp1 
	echo "start_date begin: "$start_date
	forecast_month=$(( 10#$month + 1 ))
	echo "forcast month:"$forecast_month

# FEB
	if [[ $forecast_month == 2 ]]; then 
		echo "month forcast with is FEB "
		cdo seldate,1991-01-02,1991-01-29 $tmp1 $tmp2
		start_date=$(date '+%Y%m%d ' --date="1991-02-02 00:00:00 UTC ")
# MAR 	
	elif  [[ $forecast_month == 3 ]]; then # [[ " ${month_31[*]} " =~ " $(( 10#$month - 1 )) " ]] ||
		echo "month forcast is MAR "
		cdo seldate,1991-01-02,1991-02-01 $tmp1 $tmp2
		start_date=$(date '+%Y%m%d ' --date="$start_date 00:00:00 UTC + 28 day")
# AUG or JAN
	elif [[ $forecast_month == 8 ]] || [[ $((10#$month)) == 12 ]]; then  
		echo "month forcast is AUG or JAN"
		cdo seldate,1991-01-02,1991-02-01 $tmp1 $tmp2
		start_date=$(date '+%Y%m%d ' --date="$start_date 00:00:00 UTC + 31 day")
# 	
	elif [[ " ${month_30[*]} " =~ " $(( 10#$month + 1 ))" ]]; then
		echo "month forcast with 30 days: " $forecast_month
		cdo seldate,1991-01-02,1991-01-31 $tmp1 $tmp2
		start_date=$(date '+%Y%m%d ' --date="$start_date 00:00:00 UTC + 31 day")
#		
	elif [[ " ${month_31[*]} " =~ " $(( 10#$month + 1 ))" ]]; then
		echo "month forcast with 31 days: " $forecast_month
		cdo seldate,1991-01-02,1991-02-01 $tmp1 $tmp2
		start_date=$(date '+%Y%m%d ' --date="$start_date 00:00:00 UTC + 30 day")
	fi

	start_date_cur_tmp=${start_date:0:4}"-"${start_date:4:2}"-"${start_date:6:2}

	cdo -settaxis,$start_date_cur_tmp,$start_hour,1day $tmp2 $tmp_ax1

	if [ $processed_members -gt 0 ]; then
		cdo -O mergetime  $tmp_merge_in $tmp_ax1 $tmp_merge_out
		tmp_merge_in=$tmp_merge_out
	else
		tmp_merge_in=$tmp_ax1
	fi 

	let processed_members=$processed_members+1
	echo $processed_members
	if [ $processed_members -eq 12 ]; then
		cdo -settaxis,1991-01-01,$start_hour,1day $tmp_merge_out $ensmean_year
		echo "ensmean_year: "$ensmean_year
	fi 
	echo "----------------------------"
done

delete_tmp_files