#ifndef MUTANTSTACK_HPP
#define MUTANTSTACK_HPP

#include <iostream>
#include <string>
#include <stack>
#include <deque>

using std::cout;
using std::endl;
using std::stack;

template<typename T>
class MutantStack:public stack<T>{
    public:
        MutantStack():stack<T>(){}
        MutantStack(const MutantStack& ms){
            this->c = ms.c;
        }
        MutantStack& operator=(const MutantStack& ms){
            this->c = ms.c;
            return *this;
        }
        ~MutantStack(){}
        typedef typename std::deque<T>::iterator iterator;
        iterator begin(){
            return this->c.begin();
        }
        iterator end(){
            return this->c.end();
        }
};

#endif