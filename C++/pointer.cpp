// CPP program to demonstrate 
// Overloading new and delete operator 
// for a specific class 
#include<iostream> 
#include<stdlib.h> 

using namespace std; 
class student 
{ 

public:
	string name; 
	int age; 
    char* c ;
public: 
	student() 
	{ 
		cout<< "Constructor is called\n" ; 
	} 
	student(string name, int age) 
	{ 
        cout<< "Constructor overload is called\n" ; 
		this->name = name; 
		this->age = age;
        c = new char(sizeof(name)+1);
        stpcpy(c,name.c_str());
	} 
	void display() 
	{ 
		cout<< "Name:" << name << endl; 
		cout<< "Age:" << age << endl; 
        if (c != NULL){
            cout<< "char* "<< c <<endl;
        }
            
	} 
	void * operator new(size_t size) 
	{ 
		cout<< "Overloading new operator with size: " << size << endl; 
		void * p = ::new student(); 
		//void * p = malloc(size); will also work fine 
	
		return p; 
	} 

	void operator delete(void * p) 
	{ 
		cout<< "Overloading delete operator " << endl; 
		free(p); 
	} 

    //Assignment Operator
    student& operator =(const student &s) {

        cout << "Inside assignment operator"<<endl;
        if(this != &s) 
            name = s.name;
            age = s.age;
            c = new char(sizeof(s.name)+1);
            stpcpy(c,s.name.c_str());

        return *this;
    }

    //Copy Constructor
    student (const student &s) {

        cout << "Copy  constrctor is called"<<endl;
        name = s.name;
        age = s.age;
        c = new char(sizeof(s.name)+1);
        stpcpy(c,s.name.c_str());
    }
}; 

int main() 
{ 
    // constructor and new operator will be called
	student p = student("Yash", 24); // Constuctor overload
    student p1 = student();// Constructor
    student p2 = p;// Copy constructor
    p1 = p ;// Assignment constructor
    p.name = "";
    p.age = 0;
    delete p.c;
    p.c = NULL;
	p.display(); 
    cout<< "p1****"<<endl;
	p1.display();
    cout << "p2*****"<<endl;
    p2.display();

} 
