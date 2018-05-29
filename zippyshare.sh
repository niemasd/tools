#!/bin/bash
# @Description: zippyshare.com file download script
# @Author: Live2x
# @URL: https://github.com/img2tab/zippyshare
# @Version: 201803210001
# @Date: 2018-03-21
# @Usage: sh zippyshare.sh url

if [ -z "${1}" ]
then
    echo "usage: ${0} url"
    echo "batch usage: ${0} url-list.txt"
    echo "url-list.txt is a file that contains one zippyshare.com url per line"
    exit
fi

function zippydownload()
{
    prefix="$( echo -n "${url}" | cut -c "11,12,31-38" | sed -e 's/[^a-zA-Z0-9]//g' )"
    cookiefile="${prefix}-cookie.tmp"
    infofile="${prefix}-info.tmp"

    # loop that makes sure the script actually finds a filename
    filename=""
    retry=0
    while [ -z "${filename}" -a ${retry} -lt 10 ]
    do
        let retry+=1
        rm -f "${cookiefile}" 2> /dev/null
        rm -f "${infofile}" 2> /dev/null
        wget -O "${infofile}" "${url}" \
        --cookies=on \
        --keep-session-cookies \
        --save-cookies="${cookiefile}" \
        --quiet
        filename="$( cat "${infofile}" | grep "/d/" | cut -d'/' -f5 | cut -d'"' -f1 | grep -o "[^ ]\+\(\+[^ ]\+\)*" )"
    done

    if [ "${retry}" -ge 10 ]
    then
        echo "could not download file"
        exit
    fi

    # Get cookie
    if [ -f "${cookiefile}" ]
    then 
        jsessionid="$( cat "${cookiefile}" | grep "JSESSIONID" | cut -f7)"
    else
        echo "can't find cookie file for ${prefix}"
        exit
    fi

    if [ -f "${infofile}" ]
    then
        # Get url algorithm
        dlbutton="$( grep 'getElementById..dlbutton...href' "${infofile}" | grep -m 1 -o '([0-9 \*%+\-]*)' | grep -m 1 -o '[0-9 \*%+\-]*' )"
        if [ -n "${dlbutton}" ]
        then
           algorithm="${dlbutton}" 
        else
            a="$( grep -E 'var a = [0-9][^;]*' "${infofile}" | grep -o '[0-9][^;]*' -m 1)"
            b="$( grep -E '\.omg' "${infofile}" -m 1 | grep -o '[0-9][0-9]*)' | grep -o '[0-9][0-9]*')"
            if [ -n "${b}" ]
            then
                c="$( grep -E '\.omg' "${infofile}" -m 1 | grep -o 'substr([0-9][0-9]*' | grep -o '[0-9][0-9]*')"
                b="$( echo -n $(( ${b} - ${c} )) )"
                algorithm="$( echo -n $((${a}**3+${b})) )"
            else
                echo "cound not get zippyshare url algorithm"
                exit
            fi
        fi

        a="$( echo $(( ${algorithm} )) )"
        # Get ref, server, id
        ref="$( cat "${infofile}" | grep 'property="og:url"' | cut -d'"' -f4 | grep -o "[^ ]\+\(\+[^ ]\+\)*" )"

        server="$( echo "${ref}" | cut -d'/' -f3 )"

        id="$( echo "${ref}" | cut -d'/' -f5 )"
    else
        echo "can't find info file for ${prefix}"
        exit
    fi

    # Build download url
    dl="http://${server}/d/${id}/${a}/${filename}"

    # Set brower agent
    agent="Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36"

    echo "${filename}"

    # Start download file
    wget -c -O "${filename}" "${dl}" \
    -q #--show-progress \
    --referer="${ref}" \
    --cookies=off --header "Cookie: JSESSIONID=${jsessionid}" \
    --user-agent="${agent}"

    rm -f "${cookiefile}" 2> /dev/null
    rm -f "${infofile}" 2> /dev/null
}

if [ -f "${1}" ]
then
    for url in $( cat "${1}" | grep -i 'zippyshare.com' )
    do
        zippydownload "${url}"
    done
else
    url="${1}"
    zippydownload "${url}"
fi
