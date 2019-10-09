#include<bits/stdc++.h>
using namespace std;
#define fastio ios_base::sync_with_stdio(false); cin.tie(NULL)
#define mod 1000000007
#define pb push_back 
#define pob pop_back
#define ll long long
/**************************************************************************************/
bool check(int x,int arr[][],int r,int c){
	bool flag1=flag2=flag3=flag4=0;
	for(int i=0;i<r;i++){
		for(int j=0;j<c;j++){
			
			if(i-1>0 && j-1>0 && i+1 ){
				if(arr[i-1][j]==0 || arr[i][j-1]==0 ||arr[i-1][j-1]==0 ){
					flag1 = 1;
				}
				else if(arr[i-1][j]==0 || arr[i-1][j+1]==0 ||arr[i][j+1]==0 )
					flag2 = 1;
				else if(arr[i+1][j]==0 || arr[i+1][j+1]==0 ||arr[i][j+1]==0){
					flag3 = 1;
				}
				else if(arr[i+1][j]==0 || arr[i][j-1]==0 ||arr[i+1][j-1]==0)
					flag4 = 1;
			}
		}
	}
	
	
}
int main(){
	fastio;
//	#ifndef ONLINE_JUDGE
//	freopen("input.txt","r",stdin);
//	freopen("output.txt","w",stdout);
//	#endif
	int n,m;
	cin>>n>>m;
	int arr[n][m];
	int ones[n][m]={0};
	for(int i=0;i<n;i++)
		for(int j=0;j<m;j++){
			cin>>arr[i][j];
			if(arr[i][j]==1){
				ones[i][j]=1;
			}

	for(int i=0;i<n;i++){
		for(int j=0;j<m;j++){
			if(ones[i][j]==1){
				check(arr[i][j],arr,n,m);
			}
		}
	}






return 0;
}


