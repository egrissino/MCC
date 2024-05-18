cmake_minimum_required(VERSION 3.13.0)

#project MFCC
project (MFCC LANGUAGES C)
# set(TARGET ${PROJECT_NAME})

set (CMAKE_C_STANDARD 11)

set(TARGET_NAME ${PROJECT_NAME}.app)
add_executable(${TARGET_NAME} ${SOURCES})

target_include_directories(${TARGET_NAME} PUBLIC
    ${CMAKE_CURRENT_LIST_DIR}
)

set(CONFIG_TEST_BENCH 1)

add_subdirectory(src)

if (CONFIG_TEST_BENCH)
    add_subdirectory(test)
    add_compile_definitions(TEST_BENCH)
endif()

target_link_libraries(${TARGET_NAME}
    m
)



