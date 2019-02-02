#!/bin/sh

must(){
    until "$@"
    do
        echo "sleep 1s/retry..."
	sleep 1
    done
}

must mkdir -p var
must cd var
forwardbot_var_root="$PWD"
must mkdir -p bin
must mkdir -p lib
must mkdir -p status
export LANG=zh_CN.UTF-8

must cd "$forwardbot_var_root/status"
if [ ! -f installed_coolq ]
then
    must cd "$forwardbot_var_root/bin"
    rm -fr winetricks
    must wget https://raw.githubusercontent.com/Winetricks/winetricks/master/src/winetricks
    must chmod +x winetricks
    must ./winetricks msscript
    must ./winetricks winhttp
    must ./winetricks cjkfonts

    must cd "$forwardbot_var_root/lib"
    rm -fr coolq
    must mkdir coolq
    must cd coolq
    must mkdir tmp
    must cd tmp
    must wget -O CQA.zip http://dlsec.cqp.me/cqa-tuling
    must unzip CQA.zip
    must mv *Air/* "$forwardbot_var_root/lib/coolq/"
    must cd "$forwardbot_var_root/lib/coolq"
    must rm -fr tmp

    must touch "$forwardbot_var_root/status/installed_coolq"
fi

must cd "$forwardbot_var_root/status"
if [ ! -f installed_coolq_httpapi ]
then
    must cd "$forwardbot_var_root/lib/coolq/app"
    must wget https://github.com/richardchien/coolq-http-api/releases/download/v4.7.1/io.github.richardchien.coolqhttpapi.cpk
    must touch "$forwardbot_var_root/status/installed_coolq_httpapi"
fi

must cd "$forwardbot_var_root/status"
if [ ! -f installed_python ]
then
    must cd "$forwardbot_var_root"
    must mkdir -p src/python
    must cd "$forwardbot_var_root/src/python"
    if [ ! -d Python-3.7.2 ] || [ -f Python-3.7.2.tgz ]
    then
	rm -fr *.tgz
	must wget https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tgz
	must tar -xvzf Python-3.7.2.tgz
	must rm Python-3.7.2.tgz
    fi
    must cd "$forwardbot_var_root/src/python/Python-3.7.2"
    must ./configure --enable-optimizations --prefix="$forwardbot_var_root"
    must make
    must make install

    must touch "$forwardbot_var_root/status/installed_python"
fi

must cd "$forwardbot_var_root/status"
if [ ! -f installed_pip_packages ]
then
    must "$forwardbot_var_root/bin/pip3" install wxpy
    must "$forwardbot_var_root/bin/pip3" install aiocqhttp
    must touch "$forwardbot_var_root/status/installed_pip_packages"
fi

keep_coolq(){
    while true
    do
	if killall -0 CQA.exe
	then
	else
	    rm -fr "$forwardbot_var_root/lib/coolq/data/app/io.github.richardchien.coolqhttpapi"
	    must mkdir -p "$forwardbot_var_root/lib/coolq/data/app/io.github.richardchien.coolqhttpapi/config"
	    must cp "$forwardbot_var_root/../coolq.httpapi.conf.json" "$forwardbot_var_root/lib/coolq/data/app/io.github.richardchien.coolqhttpapi/config/general.json"
	    must cd "$forwardbot_var_root/lib/coolq"
	    wine CQA.exe &
	fi
    done
}
keep_coolq &

must cd "$forwardbot_var_root/.."
"$forwardbot_var_root/bin/python3" bot.py
