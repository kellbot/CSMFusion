p=0;	// select p=1 for smooth rendering 
diam=246;
n=134; // n = number of needles
metric=true;
demoview=0;

//// uncomment components to view.
//// uncomment only one to render and generate STL file

if (demoview==0) {

//lifter();

//// section main unit

	//rotate([0,0,-15])	shell();
	//rotate([0,0,45])	shell();
	translate([0,0,8.5])
        drum();
	//rotate([0,0,-135])stationary_cam();

	//translate([0,0,10])rotate([0,0,-45])moving_cam();
//	rotate([0,0,45-15*146/diam])translate([-(diam/2)+1.5,0,41.5])knob2(20);
//	rotate([0,0,45+15*146/diam])translate([-(diam/2)+1.5,0,41.5])knob2(20);
//	rotate([0,0,45])translate([-(diam/2)-1,0,75])rotate([0,90,0])knob1(10);	//*
//	translate([0,0,-3.5])mounting();

//// section yarn guide

//	rotate([0,0,-135]){

//	rotate([0,0,-ramp])translate ([0,0,14.5])yarnpost();
//	rotate([0,0,+ramp])translate ([0,0,14.5])yarnpost();
		
//	rotate([0,0,-ramp])translate ([0,0,14.5])yarnguide();
//	rotate([0,0,+ramp])translate ([0,0,14.5])yarnguide();

//	rotate([0,0,180-ramp])translate([-(diam/2)-6.1,0,55]) knob(15);
//	rotate([0,0,180+ramp])translate([-(diam/2)-6.1,0,55]) knob(15);
//	}

//// section common

//	ballcage(diam-40.75);

}
////
//// *** NO USER INTERACTION BELOW THIS LINE ***

else {	// this produces an exploded view of the machine
	p=0;
	translate([0,0,100])shell();
	translate([0,0,180+8.5])drum();
	rotate([0,0,180])stationary_cam();
	translate([-40+0,0,50+11.5])rotate([0,0,-90])moving_cam(); //5-18
	rotate([0,0,-15*146/diam])translate([-80-(diam/2)+1.5,0,50+41.5])knob2(20);
	rotate([0,0,+15*146/diam])translate([-80-(diam/2)+1.5,0,50+41.5])knob2(20);
//	rotate([0,0,15])translate([-80-72.5,0,50+41.5]) knob2(20); // 36-48
//	rotate([0,0,-15])translate([-80-72.5,0,50+41.5]) knob2(20); // 36-48
	translate([-40-74,0,200])rotate([0,90,0])knob1(10);
	translate([0,0,-100-3.5])mounting();

	translate([0,-200,-100-3.5])drivebase();
	translate([0,-200,0])drivepulley();
	translate([0,-200,50+12])handcrank();
	translate([60,-200,70+18.5])handle();

//	rotate([0,0,-180])translate ([120+0,0,50+14.5])yarnpost();
//	rotate([0,0,-180])translate ([80+0,0,50+14.5])yarnguide();
//	rotate([0,0,0])translate([-90.1-150,0,24]) knob(15);
	
	rotate([0,0,+180]){

	rotate([0,0,-ramp])translate ([80+0,0,114.5])yarnpost();
	rotate([0,0,+ramp])translate ([80+0,0,114.5])yarnpost();
		
	rotate([0,0,-ramp])translate ([50+0,0,114.5])yarnguide();
	rotate([0,0,+ramp])translate ([50+0,0,114.5])yarnguide();

	rotate([0,0,180-ramp])translate([-100-(diam/2)-6.1,0,155]) knob(15);
	rotate([0,0,180+ramp])translate([-100-(diam/2)-6.1,0,155]) knob(15);
	}

//	translate([60+73+37.50,0,196])rotate([0,0,180])bar();
//	translate([60+73+37.50-35,0,20+196])rotate([0,-25,180])brake();
//	translate([60+73+37.50+17,1,20+196])rotate([0,45,180]) lever();
//	translate([60+73+37.50,0,-40+196])rotate([0,0,180])weight();
//	translate([60+73+37.50,0])brakebase();

	translate([0,0,-50])ballcage(diam-40.5);
	translate([0,-200,-50])ballcage((diam/2.3)-2.5);
}

////
//// ***   MODULES ARE GROUPED IN SECTIONS   ***
////

$fn=45+(p*45);
prace=45+(p*135);
pramp=45+(p*4*45);
ramp=(60*146/diam)-3;

//// section main unit

module shell(){
	difference(){
		union(){
			translate([0,0,8.3])cylinder(d=diam,h=61.70);	// shell
			translate([-(diam/2)-0,0,21])cylinder(h=49,d=8);
			translate([-(diam/2)-0,-4,21])cube([8,8,49]);
			for(i=[-1:2:1])
				rotate([0,0,180-i*ramp])
					translate([(diam/2)+1,0,40])hull(){
						translate([0,+6,0])cylinder(h=30,d=10);
						translate([0,-6,0])cylinder(h=30,d=10);
					}
		}
		translate([0,0,7]) cylinder(d=(diam-8),h=64);			// inner clearance
		for(i=[-1:2:1]){
			rotate([0,0,i*15*146/diam]){
				translate([0,0,38.5])rotate([0,-90,0])hull(){ 
					cylinder(h=diam,d=3.5);
					translate([11,0,0])cylinder(h=diam,d=3.5);
				}
				translate([-(diam/2)-1.5,-7.5,28.75]) cube([2,15,31]);
			}
			rotate([0,0,180-i*ramp]){
				translate([(diam/2)+3,0,30])hull(){
					translate([0,+4,-1])cylinder(h=42,d=6.5);
					translate([0,-4,-1])cylinder(h=42,d=6.5);
				}
				translate([0,0,56])rotate([0,90,0])cylinder(h=diam,d=2.5);
				translate([(diam/2)-5,0,56])rotate([0,90,0])cylinder(h=3,d2=2.5,d1=6);
			}
		}
		translate([0,0,60])rotate([90,0,90])cylinder(h=diam,d=2.5);	// magnet
		rotate([0,0,90]) translate([-4.25,0,26.5]) cube([8.5,diam,31]); // down-cam slot
		translate([-(diam/2)-0,0,57])cylinder(h=20,d=3);
		translate([-(diam/2)-0,0,57.5])nut();
		translate([-(diam/2)-0,0,25])cylinder(h=2.5,d=5);
		for(i=[45:90:360]){
			rotate([0,0,i])translate([(diam/2)-5,0,18])rotate([0,90,0])cylinder(h=10,d=3.5);
		}
	}
	translate([-(diam/2)-0,0,22])difference(){	// bridging brace - remove after printing
		cylinder(h=44,d=8);
		cylinder(h=60,d=6.4);
		translate([0,-4.5,0])cube([9,9,60]);
	}
}

module drum(){
	$fn=n;
	difference(){
		union(){
		cylinder(d=diam-26,h=92.5);
            // TODO
//		translate([0,0,92.5]) rotate_extrude() translate([(diam/2)-21,0,0]) circle(d=1);
		}
        
		for(i=[0:360/n:360]){  
			rotate([0,0,i]){
				translate([(diam/2)-20.5,-0.85,-1]) cube([20,1.7,77]);
				translate([(diam/2)-20.5,-1.8,75])cube([20,3.6,20]);
			}
		}
		translate([0,0,20]) cylinder(d=diam-48,h=75);

		translate([0,0,80]) cylinder(d1=diam-48,d2=diam-41,h=17);
		translate([0,0,-1])cylinder(d=diam-56, h=22);
		translate([0,0,10.01])cylinder(d1=diam-56,d2=diam-48,h=10);
		for(i=[0:360/6:360])
			rotate([0,0,i]) translate([(diam/2)-27,0,-1]) cylinder(d=6, h=12);
//		translate([0,0,58]) rotate_extrude() translate([(diam/2)-17,0,0]) circle(d=4);
//		translate([0,0,56]) rotate_extrude() translate([(diam/2)-17,0,0]) square([3.2,4]);
//	}
//	for(i=[0:360/6:360])
//		rotate([0,0,i]) translate([(diam/2)-26,0,0])
//			difference(){
//				union(){
//					cylinder(d=8, h=10);
//					translate([0,0,10])sphere(d=8);
//				}
//				translate([0,0,-1]) cylinder(d=2.5, h=11);
			}
}

module stationary_cam(){
	difference(){
		union(){
			difference(){
//				cylinder(h=9,d=diam);
				beltwheel(2*floor(PI*(diam)/4));
				translate([0,0,8]) cylinder(h=2,d=diam+10);
			}
			rotate([0,0,ramp])lifter();
			rotate([0,0,-ramp])lifter();
			rotate([0,0,ramp])
				rotate_extrude(angle=360-ramp-ramp-6)
						translate([(diam-25)/2,0])square([7.75,30]);
		}
		translate([0,0,-1]) cylinder(d=diam-38.5,h=10);	// base clearance
		translate([0,0,4])
			rotate_extrude(angle=360, $fn=prace) translate([(diam/2)-20.375,0])circle(d=4.5);
		for(i=[45:90:360])
			rotate([0,0,i])translate([0,0,18])rotate([0,90,0])cylinder(h=diam,d=2.5);
		rotate([0,0,ramp])lifterguide();
		rotate([0,0,-ramp])lifterguide();
	}
}
	
module moving_cam(){
	difference(){
		union(){
			translate([0,0,51])rotate([0,180,90])lifter();
			translate([0,-(diam/2)-1,20])cylinder(h=20,d=8);
			translate([-4,-(diam/2)-1,20]) cube([8,8,20]);
		}
		translate([0,0,51])rotate([0,180,90])lifterguide();
		rotate([0,0,15*146/diam])translate([0,-(diam/2)+13,32]) rotate([90,0,0]) cylinder(d=3.2,h=13);
		rotate([0,0,-15*146/diam])translate([0,-(diam/2)+13,32]) rotate([90,0,0]) cylinder(d=3.2,h=13);
		rotate([0,0,15*146/diam])translate([0,-(diam/2)+13,32]) rotate([90,0,0]) nut();       
		rotate([0,0,-15*146/diam])translate([0,-(diam/2)+13,32]) rotate([90,0,0]) nut();       
		translate([0,-(diam/2)-1,19])cylinder(h=12,d=5);
		translate([0,0,43])cylinder(h=10,d=diam);
	}
	rotate([0,0,90])translate([-(diam/2)-1,0,40])difference(){	// bridging brace - remove after printing
		cylinder(h=3,d=8);
		cylinder(h=60,d=6.4);
		translate([0,-4.5,0])cube([9,9,60]);
	}
}

module lifter(){
	module segment(){
		difference(){
			circle(d=diam-9.5);
			circle(d=diam-25);
			translate([-diam,-diam/2])square(diam);
		}	
	}
	intersection(){
		rotate([0,0,-90+ramp])linear_extrude(height=45,twist=ramp, $fn=pramp)
			segment();
		rotate([0,0,90-ramp])linear_extrude(height=45,twist=-ramp, $fn=pramp)
			segment();
	}
}

module lifterguide() {
	rotate([0,0,+ramp])linear_extrude(height=45,twist=ramp, $fn=pramp)
		translate([(diam/2)-10,-0.3,0])
		scale([1,1.4])square(0.8);
		rotate([0,0,-ramp])linear_extrude(height=45,twist=-ramp, $fn=pramp)
			translate([(diam/2)-10,-0.7,0])
			scale([1,1.4])square(0.8);
}

module knob(size){
	translate([-5,0,0])rotate([0,90,0]){
		difference(){
			union(){
				cylinder(h=4,d=size);
				cylinder(h=5,d=size*0.6);
			}
			cylinder(h=14,d=3.5);
			translate([0,0,-1])nut();
		}
	for(i=[0:18:360]) rotate([0,0,i])translate([size/2,0,0.5]) cylinder(h=3,d=2);
	}
}

module knob1(size){
	translate([-5,0,0])rotate([0,90,0]){
		difference(){
			union(){
				cylinder(h=7.5,d=size);
				for(i=[0:18:360]) rotate([0,0,i])translate([size/2,0,0.5]) cylinder(h=6.5,d=2);
				}
			cylinder(h=14,d=2.5);
			translate([0,0,-1])cylinder(h=3,d=6);
			translate([0,0,-1])rotate([0,-90,0])cylinder(h=10,d=3,$fn=4);
		}
	}
}

module knob2(size){
	translate([-5,0,0])rotate([0,90,0]){
		difference(){
			union(){
				cylinder(h=4,d=size);
				cylinder(h=6,d=size*0.6);
			}
			cylinder(h=14,d=2.5);
			translate([0,0,-1])cylinder(h=3,d=6);
		}
	for(i=[0:18:360]) rotate([0,0,i])translate([size/2,0,0.5]) cylinder(h=3,d=2);
	}
}


module mounting () {
	difference(){
		union(){
			difference(){
				union() {
					cylinder(d=diam-43,h=12);
					hull()
						for(i=[0:360/4:359])
							rotate([0,0,i]) translate([((diam-25)*0.70),0,0]) cylinder(h=2.5,d=25);
				}
				translate([0,0,-1]) cylinder(d=diam-56,25);
			}
			for(i=[0:360/6:359])
				rotate([0,0,i]) translate([(diam/2)-26,0,0]) cylinder(h=12,d=8);
		}
		for(i=[0:360/6:360])
			rotate([0,0,i]) {
				translate([(diam/2)-26,0,-1]){
					cylinder(d=3.5,h=14.5);
					cylinder(d=6, h=4);
				}
			}
		for(i=[0:360/4:359]) 
			rotate([0,0,i]) 
				translate([((diam-25)*0.7),0,-1]) cylinder(h=6, d=4);
		translate([0,0,7.5]) 
			rotate_extrude(angle=360, $fn=prace) translate([(diam/2)-20.375,0])circle(d=4.5);
	}
}


module beltwheel(teeth) {
	cylinder(h=9, d=((teeth*2)/PI)-2.5);
	for(i=[0:360/teeth:360]){
		rotate([0,0,i]) cube([0.8,(teeth/PI)-0.5,9]);
	}
	cylinder(h=0.8, d=((teeth*2)/PI)+0.5);
	translate([0,0,8.2])cylinder(h=0.8, d=((teeth*2)/PI)+0.5);
}


//// section yarnguide

module yarnpost() {
	difference(){	//stem
		union(){
			translate([(diam/2)+3,0,0])
				hull(){
					translate([0,+4,30])cylinder(h=62,d=6);
					translate([0,-4,30])cylinder(h=62,d=6);
				}
			translate([(diam/2),0,103])rotate([90,0,90])
				hull(){
					translate([5,-9.5,0])cylinder(h=20,d=8);
					translate([-5,-9.5,0])cylinder(h=20,d=8);
				}
			}
		translate([(diam/2)-1,0,102])rotate([90,0,90])
			hull(){
				translate([3,-7,0])cylinder(h=22,d=5.2);
				translate([-3,-7,0])cylinder(h=22,d=5.2);
			}
		translate([(diam/2)+9,0,88])cylinder(h=10,d=2.5);
		translate([(diam/2)-1,0,40])rotate([0,90,0])
			hull(){
				translate([15,0,0])cylinder(h=10,d=4);
				translate([-5,0,0])cylinder(h=10,d=4);
			}
	}
}

module yarnguide(){
	translate([5,0,90]){
		intersection(){
			translate([(diam/2)-28,0,25])rotate([0,90,0])cylinder(h=20,d=50);
			translate([(diam/2)-28,0,-27])rotate([0,90,0])cylinder(h=20,d=90);
			difference(){
				cylinder(h=25,d=diam-34);
				translate([0,0,-1])cylinder(h=27,d=diam-36);
				translate([(diam/2)-33,00,12])rotate([0,90,0])cylinder(h=20,d=3);
				translate([(diam/2)-23,-0.5,12])cube([10,1,10]);
				translate([(diam/2)-23,-15,-7.5])cube([10,30,10]);
			}
		}
	}

	translate([(diam/2)-13,0,102])rotate([90,0,90]){
		difference(){
			hull(){
				translate([3,-7,0])cylinder(h=36,d=5);
				translate([-3,-7,0])cylinder(h=36,d=5);
			}
		translate([0,-10,22])rotate([0,90,90])
			hull(){
				translate([5,0,0])cylinder(h=7,d=3.5);
				translate([-5,0,0])cylinder(h=7,d=3.5);
			}
				translate([-2.5,-3,34])rotate([90,0,0])cylinder(h=7,d=1);
				translate([2.5,-3,34])rotate([90,0,0])cylinder(h=7,d=1);
		}
	}
}

////section common

module ballcage(cdiam) {
	balls=floor(PI*cdiam/10);
	difference(){
		cylinder(h=6, d=cdiam+1.2);
		translate([0,0,-1])cylinder(h=10, d=cdiam-1.2);
		for(i=[0:360/balls:360]){  
			rotate([0,0,i]) translate([0,0,4])rotate([90,0,0]) cylinder(h=diam,d=5); 
		} 
	}
}

module nut(){
	if (metric==true) 	// M3 
		cylinder(h=3,d=6.35,$fn=6);
	else	// #4 UNC
		cylinder(h=3,d=7.35,$fn=6);
}