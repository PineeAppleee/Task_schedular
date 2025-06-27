Interactive JIT Compiler & Virtual MachineThis project is a complete, interactive Just-In-Time (JIT) compiler and virtual machine for a custom, stack-based assembly language. It features a C++ backend for high-performance execution and a modern web-based user interface for writing, running, and visualizing scripts.A Node.js server acts as the bridge between the web frontend and the C++ backend, allowing you to run compiled code from the comfort of your browser.

Features

 . Interactive Web UI: A clean, modern frontend built with HTML and Tailwind CSS to write and execute scripts
 
 . Real-time Visualization: See the final state of the VM's stack, variables, and output after every execution
 
 . C++ Core: The tokenizer, parser, and virtual machine are written in C++ for performance
 
 . Rich Assembly Language: Supports variables, functions, loops, conditional logic, and even array manipulation
 
 . Client-Server Architecture: Demonstrates a practical architecture for connecting a web frontend to a native backend executable
 
Architecture
  
The project is composed of three main parts that work together:
Frontend (index.html): The user interface that runs in the browser. When you click "Run on Server", it sends the script from the editor to the Node.js server.

Node.js Server (server.js): A lightweight backend that listens for requests from the frontend. It receives the script, executes the C++ compiler as a child process, captures its output, and sends the result back to the frontend as JSON.

C++ Backend (jit_compiler executable): The core of the project. It takes a script as a command-line argument, tokenizes it, parses it into instructions, executes it in a virtual machine, and prints the final state of the VM as a JSON string to standard output.


+----------------+      HTTP POST Request      +-------------------+      Execute Command      +---------------------+
|   Web UI       |   (with script payload)    |   Node.js Server  |   (e.g., ./jit_compiler)   |   C++ Executable    |
|  (index.html)  | -------------------------> |    (server.js)    | -------------------------> |    (jit_compiler)   |
|                | <------------------------- |                   | <------------------------- |                     |
+----------------+     JSON Response with     +-------------------+       JSON Output via      +---------------------+
                     Execution Result                             Standard Output

                     
How to Run the Project

Follow these steps to compile and run the project on your local machine.PrerequisitesA C++ compiler that supports C++17 (like g++ or clang++).
Node.js installed on your system.

Step 1: Compile the C++ BackendOpen a terminal in the root of your project folder and run the following command to compile all the C++ source files into a single executable.
g++ main.cpp vm.cpp parser.cpp -o jit_compiler -std=c++17

Note: If you are on Windows, you may want to name the output jit_compiler.exe and update the JIT_EXECUTABLE variable in server.js accordingly.

Step 2: Install Node.js DependenciesIf you haven't already, install the express library, which is used by the server.npm install express

Step 3: Start the ServerRun the Node.js server from your terminal.node server.js

You should see a message confirming that the server is running: Server listening at http://localhost:3000

Step 4: Use the Web InterfaceOpen your favorite web browser and navigate to the following 
URL:http://localhost:3000
