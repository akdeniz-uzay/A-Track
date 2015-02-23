#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
/* 							 04/12/2013	*/
/* flux/background karşılaştırması iptal!				*/
/* bütün frame'lerdeki bütün komşulukları etiketleyerek tek dosyaya yazar (err2).
   (aynı frame'deki komşuluklar ihmal edilerek!)
*/
#define MAX1 5000
#define MAX2 45000

int main( int argc, char *argv[])
{
int err=1,sourcecount1=0,sourcecount2=0,sourcecount3=0,i=0,k,count_matched=0,f,total,j;
int id1[MAX1],id2[MAX1],id3[MAX2],id4[MAX2],flag1[MAX1],flag2[MAX1],flag3[MAX2],flag4[MAX2];
double x1[MAX1],y1[MAX1],flux1[MAX1],background1[MAX1],rec1[MAX1],dec1[MAX1];
double x2[MAX1],y2[MAX1],flux2[MAX1],background2[MAX1],rec2[MAX1],dec2[MAX1];
double x3[MAX2],y3[MAX2],flux3[MAX2],background3[MAX2],rec3[MAX2],dec3[MAX2];
double x4[MAX2],y4[MAX2],flux4[MAX2],background4[MAX2],rec4[MAX2],dec4[MAX2];
//double x5[MAX],y5[MAX],flux5[MAX],background5[MAX],rec5[MAX],dec5[MAX];
double diffx, diffy, diff, dist, distij, distik, distjk, height, s,range=1.0,pixel_range=20;
int count1=0,count2=0,count3=0,count4=0, candidates =0;

FILE *DOSYA1, *DOSYA2, *DOSYA3;
char file1[30]; char file2[30]; char file3[]="all_xyrd11.txt";

DOSYA3=fopen(file3,"w");

	sscanf(argv[1],"%s",file1);
	DOSYA1=fopen(file1,"r");
/*%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%*/
/* 			I. DOSYA					*/
	fscanf(DOSYA1,"%*s %*s %*s %*s %*s %*s");
	while( err!=EOF){
		err = fscanf(DOSYA1,"%d %lf %lf %lf %lf %*d %lf %lf",&id1[i],&x1[i],&y1[i],&flux1[i],&background1[i],&rec1[i],&dec1[i]);
		flag1[i] = 0; flag3[i] = 0;
//		if(background1[i] < flux1[i]){ //background'dan küçük olanlar ihmal ediliyor!
			id3[i]=1; x3[i]=x1[i]; y3[i]=y1[i]; rec3[i]=rec1[i]; dec3[i]=dec1[i];
			flux3[i] = flux1[i];background3[i]=background1[i];
			i++;
		//}
	}
	sourcecount1 = i-1;total = sourcecount1;
/*%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%*/
	i = 0; err = 1; // err, sonraki dosyayı okuması için tekrar 1 yapılmalı!
/* 			SONRAKI DOSYALAR				*/
for(f=2;f<argc;f++){
	sscanf(argv[f],"%s",file2);
	
	DOSYA2=fopen(file2,"r");
	fscanf(DOSYA2,"%*s %*s %*s %*s %*s %*s ");
	while( err!=EOF){
		err = fscanf(DOSYA2,"%d %lf %lf %lf %lf %*d %lf %lf",&id2[i],&x2[i],&y2[i],&flux2[i],&background2[i],&rec2[i],&dec2[i]);
		flag2[i] = 0; flag3[total+i] = 0;
//		if(background2[i] < flux2[i]){ //background'dan küçük olanlar ihmal ediliyor!
			id3[total+i]=f; 
			x3[total+i]=x2[i]; y3[total+i]=y2[i]; 
			rec3[total+i]=rec2[i]; dec3[total+i]=dec2[i];
			flux3[total+i] = flux1[i];background3[total+i]=background1[i];
			i++;
	//	}
	}
	sourcecount2 = i-1;total += sourcecount2;
/*%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%*/
	i = 0; err = 1; // err, sonraki dosyayı okuması için tekrar 1 yapılmalı!
	count_matched=0;
	fclose(DOSYA2);
}
/*%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%*/
	for(i=0;i<total;i++){	
		for(j=0;j<total;j++){	
			//if(fabs(x3[i]-x3[j])<5.0 && fabs(y3[i]-y3[j])<5.0  && fabs(x3[i]-x3[j])>1.0 && fabs(y3[i]-y3[j])>1.0 && id3[i] != id3[j])
			if(fabs(x3[i]-x3[j])<6.0 && fabs(y3[i]-y3[j])<6.0 && id3[i] != id3[j])
                                flag3[i] += 1;	
		}
	}/**/
	candidates = 0;
	for(i=0;i<total;i++){
		if( flag3[i] >1 &&  flag3[i] <6){
			id4[candidates] = id3[i];
			x4[candidates] = x3[i];
			y4[candidates] = y3[i];
			rec4[candidates] = rec3[i];
			dec4[candidates] = dec3[i];
			flag4[candidates] = 0;
			candidates++;
		}
	}
	
	 for(i=0;i<candidates;i++){
	 	for(j=i+1;j<candidates;j++){
			if( id4[i] != id4[j] ){
	 			for(k=j+1;k<candidates;k++){
					if( id4[i] != id4[k] && id4[j] != id4[k] ){ /* uc nokta da farklı dosyalardan */
						if(fabs(x4[i]-x4[k])<pixel_range && fabs(y4[i]-y4[k])<pixel_range && 
					   	   fabs(x4[i]-x4[j])<pixel_range && fabs(y4[i]-y4[j])<pixel_range && 
					   	   fabs(x4[j]-x4[k])<pixel_range && fabs(y4[j]-y4[k])<pixel_range ){
							
							diffx = pow(x4[i]-x4[j],2); diffy = pow(y4[i]-y4[j],2);
							distij =sqrt(diffx + diffy);
							diffx = pow(x4[i]-x4[k],2); diffy = pow(y4[i]-y4[k],2);
							distik =sqrt(diffx + diffy);
							diffx = pow(x4[j]-x4[k],2); diffy = pow(y4[j]-y4[k],2);
							distjk =sqrt(diffx + diffy);
							if(distij>distik && distij>distjk){	
								height= fabs( (x4[j]-x4[i])*y4[k] 
									+  (y4[i]-y4[j])*x4[k] + x4[i]*y4[j] 
									- x4[j]*y4[i])/sqrt(pow(x4[j]-x4[i],2)+pow(x4[j]-x4[i],2));
								dist = distij;
							}
							if(distik>distij && distik>distjk){	
								height= fabs( (x4[k]-x4[i])*y4[j] 
									+  (y4[i]-y4[k])*x4[j] + x4[i]*y4[k] 
									- x4[k]*y4[i])/sqrt(pow(x4[k]-x4[i],2)+pow(x4[k]-x4[i],2));
								dist = distik;
							}
							if(distjk>distik && distjk>distij){	
								height = fabs( (x4[j]-x4[k])*y4[i] 
									+  (y4[k]-y4[j])*x4[i] + x4[k]*y4[j] 
									- x4[j]*y4[k])/sqrt(pow(x4[j]-x4[k],2)+pow(x4[j]-x4[k],2));
								dist = distjk;
							}

							s = 0.5*fabsl(x4[i]*y4[j]+x4[j]*y4[k]+x4[k]*y4[i]-(y4[i]*x4[j]+y4[j]*x4[k]+y4[k]*x4[i]));
							if(s<1.0 && height <1.0 && dist>2.0){
								flag4[i] += 1; flag4[j] += 1;flag4[k] += 1;
printf("%d %d %d %d %5.13f %5.13f %5.13f %5.13f %5.13f %5.13f %f %f %d %f %f %f\n",i,j,k,id4[k],rec4[i],dec4[i],rec4[j],dec4[j],rec4[k],dec4[k],x4[k],y4[k],flag4[i],dist,height,s);
							count1++;
							}
						}
		     			}			
				}
			}
		}
	}/**/
	 for(i=0;i<candidates;i++){
		if(flag4[i] >= 10){
			fprintf(stderr,"%d %d %5.13f %5.13f  %5.13f %5.13f %d\n",i,id4[i],rec4[i],dec4[i],x4[i],y4[i],flag4[i]);
		}
	}
	
	printf("count1:%d \n",count1);

	for(i=0;i<total;i++){	
			fprintf(DOSYA3,"%d %5.5f %5.5f %5.13f %5.13f %d %5.3f %5.3f\n",id3[i],x3[i],y3[i],rec3[i],dec3[i],flag3[i],flux3[i],background3[i]);
			
	}

	fclose(DOSYA3);
return 0;
}
