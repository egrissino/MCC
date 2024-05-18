timestamp=$(echo $(date +%d.%m.%y-%H:%M:%S))
echo $timestamp
echo $project
mkdir -p build
cd build
cmake --build ./ | tee build.log
if [[ $? == "0" ]] ; then
    echo "Build Succeeded"
    mkdir -p logs
    ./${project}.${extension} | tee >> ./logs/${project}_log_${timestamp}.txt
    cp ./logs/${project}_log_${timestamp}.txt ./${project}_log.txt
    cat ./${project}_log.txt
    
fi
exit