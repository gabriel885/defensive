cmake_minimum_required(VERSION 3.13)
project(client)

set(CMAKE_CXX_STANDARD 11)

set(CMAKE_CXX_FLAGS "-g -Wall -std=c++11")


set(HEADERS ./include)

set(SOURCE_FILES
         src/main.cpp)

#set(SOURCE_FILES
#        src/c-client.cpp )
#
#set(XMLRPC_C_INCLUDE_DIRS
#        ./libs/xmlrpc-c-1.51.06/include
#        )

find_package(XMLRPC REQUIRED libwww-client)

include_directories(
        ${HEADERS}
        ${XMLRPC_INCLUDE_DIRS}
        )


add_executable(client ${SOURCE_FILES})


target_link_libraries(client ${XMLRPC_LIBRARIES})
