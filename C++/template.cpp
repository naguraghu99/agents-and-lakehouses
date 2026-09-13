#include <iostream> 
using namespace std; 

// One function works for all data types. This would work 
// even for user defined types if operator '>' is overloaded 
template <typename T,typename S> 
S myMax(T x, S y) 
{ 
return (x > y)? x: y; 
} 
template <>
string myMax(string s, string t){
    cout << "template specilaization"<<endl;
    return (s.length() > t.length()) ? s:t;
}

int main() 
{ 
cout << myMax<int,double>(3, 7) << endl; // Call myMax for int 
cout << myMax<double,double>(3.0, 7.0) << endl; // call myMax for double 
cout << myMax<char,char>('g', 'e') << endl; // call myMax for char 
cout << myMax<string,string>("nagu","jai")<<endl;

return 0; 
}
