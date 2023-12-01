////****** User Settings ************************************************

//select M3 or #4 UNC
metric=true;
//exploded view
demoview=true;
//cylinder diameter
Csize=120; // [75:300]
//number of needles
needles=64; // [48:2:144] 
//up and down cam anges
rampangle=53; // [40:60] 



////****** User Selection ************************************************
//// use ucustomizer (uncheck Window-Hide Customizer)	
//// or type change false to true to view a component.
//// select only one to render and generate STL file


/* [section main] */

show_shell=false;
show_cylinder=false;
show_up_cam=false;
show_down_cam=false;
show_side_knob1=false;
show_side_knob2=false;
show_top_knob=false;
show_main_pulley=false;
show_main_base=false;
show_ballcage_outer=false;
show_ballcage_inner=false;

/* [section crank drive] */

show_drive_base=false;
show_drive_pulley=false;
show_drive_crank=false;
show_drive_handle=false;
show_ballcage_crank=false;

/* [section yarn guide] */

show_yarn_base=false;
show_yarn_post=false;
show_yarn_guide=false;
show_yarn_knob=false;

/* [section yarn brake / heel spring] */

show_brake_bar=false;
show_brake_brake=false;
show_brake_lever=false;
show_brake_weight=false;
show_brake_base=false;

////***** End User Selection ********************************************
////
//// *** NO USER INTERACTION BELOW THIS LINE ***
//// *** unless you know what you are doing! ***

Ssize=Csize+26;		// shell diameter
hCsize=Csize/2;		// cylinder radius
hSsize=Ssize/2;		// shell radius
ramp=(rampangle*120/Csize)-3;

	echo("overall size:",Csize+60);

if (demoview==false) {


//// section main unit

if(show_shell==true) rotate([0,0,0])	shell();
if(show_cylinder==true) translate([0,0,8.5])drum();
if(show_up_cam==true) rotate([0,0,180])up_cam();
if(show_down_cam==true) translate([0,0,7])rotate([0,0,-90])down_cam();
if(show_side_knob1==true) rotate([0,0,-15*120/Csize])translate([-hSsize+0.5,0,41.5])knob(6,4,20,false);
if(show_side_knob2==true) rotate([0,0,+15*120/Csize])translate([-hSsize-0.5,0,41.5])knob(6,4,20,false);
if(show_top_knob==true) translate([-hSsize-1,0,75])rotate([0,90,0])knob(7.5,7.5,10,false);
if(show_main_pulley==true) rotate([0,0,180-asin(31/Ssize)])mainpulley();
if(show_main_base==true) translate([0,0,-3.5])base();
if(show_ballcage_outer==true) color("red")ballcage(Ssize+2.25);		// outer
if(show_ballcage_inner==true) color("red")ballcage(Ssize-36);		// inner


//// section crank drive

if(show_drive_base==true) translate([0,-200,-3.5])drivebase();
if(show_drive_pulley==true) translate([0,-200,0])drivepulley();
if(show_drive_crank==true) translate([0,-200,12])handcrank();
if(show_drive_handle==true) translate([0,-200,18.5])handle();
if(show_ballcage_crank==true)  translate([0,-200,0.5])color("red")ballcage(Ssize/2.3);		// crank


//// section yarn guide

if(show_yarn_base==true) rotate([0,0,-180])translate ([0,0,8])yarnbase();
if(show_yarn_post==true) rotate([0,0,-180])translate ([0,0,14.5])yarnpost();
if(show_yarn_guide==true) rotate([0,0,-180])translate ([0,0,14.5])yarnguide();
if(show_yarn_knob==true) translate([-hSsize-17.5,0,24]) knob(5,4,15,true);


//// section yarn brake / heel spring

if(show_brake_bar==true) translate([73+37.50,0,296])rotate([0,0,180])bar();
if(show_brake_brake==true) translate([73+37.50-35,0,296])rotate([0,-25,180])brake();
if(show_brake_lever==true) translate([73+37.50+17,1,296])rotate([0,45,180])lever();
if(show_brake_weight==true) translate([73+37.50,0,-40+296])rotate([0,0,180])weight();
if(show_brake_base==true) translate([73+37.50,0])brakebase();

//// section tools (WIP)

//	basket();

////section sensor

//	translate([0,0,60])	magnet(17);
//	translate([73+37.5,0,90])rotate([0,0,-90])display();
//	translate([73+37.5,0,90])rotate([0,0,-90])display1();
//	translate([73+37.5,0,90])rotate([0,0,-90])displaymount();
//	translate([73+37.5,0,63])rotate([0,0,180])reedsensor();
}

else {	// this produces an exploded view of the machine
	translate([0,0,120])shell();
	translate([0,0,200+8.5])drum();
	translate([0,0,50])rotate([0,0,180])up_cam();
	translate([0,0,50+11.5])rotate([0,0,-90])down_cam(); //5-18
	rotate([0,0,15*120/Csize])translate([-40-hSsize,0,50+41.5]) knob(6,4,20,false);
	rotate([0,0,-15*120/Csize])translate([-40-hSsize,0,50+41.5]) knob(6,4,20,false);
	translate([-hSsize,0,200])rotate([0,90,0])knob(7.5,7.5,10,false);
	translate([0,0,-100-3.5])base();
	rotate([0,0,144])mainpulley();

	translate([0,-Ssize,-100-3.5])drivebase();
	translate([0,-Ssize,0])drivepulley();
	translate([0,-Ssize,50+12])handcrank();
	translate([0,-Ssize,70+18.5])handle();
	translate([0,-Ssize,-50])ballcage(Ssize/2.3);

	rotate([0,0,-180])translate ([70,0,8])yarnbase();
	rotate([0,0,-180])translate ([70,0,50+14.5])yarnpost();
	rotate([0,0,-180])translate ([70-40,0,50+14.5])yarnguide();
	rotate([0,0,0])translate([-hSsize-100,0,24]) knob(5,4,15,true);

//	translate([60+73+37.50,0,196])rotate([0,0,180])bar();
//	translate([60+73+37.50-35,0,20+196])rotate([0,-25,180])brake();
//	translate([60+73+37.50+17,1,20+196])rotate([0,45,180]) lever();
//	translate([60+73+37.50,0,-40+196])rotate([0,0,180])weight();
//	translate([60+73+37.50,0])brakebase();

	translate([0,0,-50])ballcage(Ssize-36);
	translate([0,0,-50])ballcage(Ssize+2.25);
}

////
//// ***   MODULES ARE GROUPED IN SECTIONS   ***
////

$fn = $preview ? 45 : 90;
prace = $preview ? 45 : 180;
pramp = $preview ? 45 : 90;


//// section main unit

module shell(){
	difference(){
		union(){
			rotate_extrude(angle=360,convexity=10)		// shell body
				translate([hSsize-4,8.3])square([4,61.70]);
			translate([-hSsize-1,0,21])cylinder(h=49,d=8);	// down cam support
			translate([-hSsize-1,-4,21])cube([5,8,49]);
			for(i=[-1:2:1]){		// bumpers
				rotate([0,0,180-i*(ramp+9)]){
					translate([0,0,16.3])
						rotate_extrude (angle=i*8)
							translate([hSsize,0,0]) 
								difference(){
									circle(d=10);
									translate([-10,-5])square(10);
							}
					translate([hSsize,0,16.3])
							difference(){
								sphere(d=10);
								translate([-10,-5,-5])cube(10);
							}
				}
			rotate([0,0,i*15*120/Csize])			// down cam screw flats
				translate([-hSsize+4,0,38.5])rotate([0,-90,0])
					hull(){ 
						cylinder(h=4,d=16);
						translate([11,0,0])cylinder(h=4,d=16);
					}
				}
		}
//		translate([0,0,+7]) cylinder(d=(Ssize-8),h=64);			// inner diameter
		for(i=[-1:2:1])
			rotate([0,0,i*15*120/Csize])			// down cam screw slots
				translate([0,0,38.5])rotate([0,-90,0])
					hull(){ 
						cylinder(h=Ssize,d=3.5);
						translate([11,0,0])cylinder(h=Ssize,d=3.5);
					}
		rotate([0,0,90]) translate([-4.25,0,26.5]) cube([8.5,Ssize,31]);	// down_cam cutout
		translate([0,0,60])rotate([90,0,90])cylinder(h=Ssize,d=2.5);			// magnet (WIP)
		translate([-hSsize-1,0,57])cylinder(h=20,d=3);		// down cam adjuster 
		translate([-hSsize-1,0,57.5])nut();
		translate([-hSsize-1,0,25])cylinder(h=2.5,d=5);
		for(i=[45:45:315])		// attachment holes, to mate with up-cam
			rotate([0,0,i+180])translate([hSsize-5,0,25])rotate([0,90,0])cylinder(h=10,d=3.5);
	}
	
if (demoview==false)
	translate([-hSsize-1,0,8.3])difference(){	// bridging brace - remove after printing
		cylinder(h=50,d=8);
		cylinder(h=60,d=6.4);
		translate([0,-4.5,0])cube([9,9,60]);
	}
}

module drum(){		// cylinder is taken :-(
	
	module template(gap){		// vertical projection
				difference(){
					circle(d=Csize);
					for(i=[0:360/needles:359])
						rotate([0,0,i])
							translate([hCsize-7.5,-gap/2]) square([20,gap]);
						circle(d=Csize-17);
				}
	}
		
	difference(){
		union(){
			linear_extrude(72.5, convexity = 10) template(1.7);		// upper part
			linear_extrude(92.5) template(3.8);		// lower part
			rotate_extrude(){
				polygon(points=[[hCsize-8,0],[hCsize-15,0],[hCsize-15,12],[hCsize-11,22],
											 [hCsize-11,80],[hCsize-8.5,92.5],[hCsize-8,92.5]]);
				translate([hCsize-8,92.5]) circle(d=1);	// top round off
			}
			for(i=[0:360/6:359])		// mount points
				rotate([0,0,i]) translate([hCsize-13,0,0]){
					cylinder(d=8, h=10);
					translate([0,0,10])sphere(d=8);
				}
		}
		rotate_extrude(angle=360){
			translate([hCsize-4,65]) circle(d=4);		// recess for rubber band
			if (demoview==false) 
				translate([hCsize-4,63]) square([3.2,4]);
			else
				translate([hCsize-4,63]) square([5.2,4]);
		}
		for(i=[0:360/6:359])		// mount points
			rotate([0,0,i]) translate([hCsize-13,0,0])
				translate([0,0,-1])cylinder(d=2.5, h=13);
	}
}

module up_cam(){
	difference(){
		union(){
			difference(){
				union(){
					translate([0,0,4])rotate_extrude(angle=360,$fn=prace)		// bottom plate
						translate([hSsize-18+1.125,0])
							difference(){
								translate([0,-4])square([18-1.125,8]);
								translate([-1.125,0])circle(d=4.5);
								translate([18,0])circle(d=4.5);
							}
					rotate([0,0,ramp])
						rotate_extrude(angle=360-2*ramp)		// semi circle half height needle rest
							translate([hSsize-12.5,0])square([7.75,30]);
				}
				rotate([0,0,ramp-3])lifterguide();		// recesses for wire bearing
				rotate([0,0,-ramp+3])lifterguide();
			}
			rotate([0,0,ramp-3])lifter();		// left and right cams
			rotate([0,0,-ramp+3])lifter();
		}
		for(i=[45:45:359])
			rotate([0,0,i])translate([0,0,25])rotate([0,90,0])cylinder(h=Ssize,d=2.5);
	}
}
	
module down_cam(){
	difference(){
		union(){
			translate([0,0,51])rotate([0,180,90])lifter();		// cam
			translate([0,-hSsize-1,20])cylinder(h=20,d=8);		// guide
			translate([-4,-hSsize-1,20]) cube([8,8,20]);
		}
//		translate([0,0,51])rotate([0,180,90])lifterguide();		// recess for wire bearing
		for(i=[-1:2:1]) {		// attachment holes
			rotate([0,0,i*15*120/Csize])
				translate([0,-hSsize+13,32]) rotate([90,0,0]) cylinder(d=3.2,h=13);
			rotate([0,0,i*15*120/Csize])
				translate([0,-hSsize+13,32]) rotate([90,0,0]) nut();
		}
		translate([0,-hSsize-1,19])cylinder(h=12,d=5);		// recess for spring
		translate([0,0,43])cylinder(h=10,d=Ssize);		// cut off oversize
	}
	if (demoview==false) {
		rotate([0,0,90])translate([-hSsize-1,0,40])difference(){	// bridging brace - remove after printing
			cylinder(h=3,d=8);
			cylinder(h=60,d=6.4);
			translate([0,-4.5,0])cube([9,9,60]);
		}
	}
}


module lifter(){
	module segmenta(){
		difference(){
			circle(d=Ssize-9.5);
			circle(d=Ssize-25);
			translate([-Ssize,-hSsize])square(Ssize);
			translate([0,hSsize-10])scale([1.4,1])circle(d=0.8);
//			translate([0,-hSsize+9.5])scale([1.4,1])circle(d=0.8);
		}
	}
	module segmentb(){
		difference(){
			circle(d=Ssize-9.5);
			circle(d=Ssize-25);
			translate([-Ssize,-hSsize])square(Ssize);
//			translate([0,hSsize-9.5])scale([1.4,1])circle(d=0.8);
			translate([0,-hSsize+10])scale([1.4,1])circle(d=0.8);
		}
	}
	intersection(){
		rotate([0,0,-90+ramp])linear_extrude(height=45,twist=ramp, convexity = 10, $fn=pramp)
			segmenta();
		rotate([0,0,90-ramp])linear_extrude(height=45,twist=-ramp, convexity = 10, $fn=pramp)
			segmentb();
	}
}

module lifterguide() {
	rotate([0,0,+ramp])linear_extrude(height=45,twist=ramp, $fn=pramp)
		translate([hSsize-10,0])scale([1,1.4])circle(d=1.2);
	rotate([0,0,-ramp])linear_extrude(height=45,twist=-ramp, $fn=pramp)
		translate([hSsize-10,0])scale([1,1.4])circle(d=1.2);
}

module knob(ht1,ht2,di,nu){		// total height, knob height, knob diameter, nut (not bolt)
	ribs=360/floor(PI*di/4);
	translate([-ht1,0,0])rotate([0,90,0]){
		difference(){
		union(){
			cylinder(h=ht2,d=di);
			cylinder(h=ht1,d=di*0.6);
		}
		translate([0,0,-1]){
			if(nu==true){
				cylinder(d=3.5,h=ht1+2);
				nut();
			}
			else {
				cylinder(d=2.5,h=ht1+2);
				cylinder(d=6.5,h=3);
			}
		}
	}		// knobbely bits
	for(i=[0:ribs:359]) rotate([0,0,i])translate([di/2,0,0.5]) cylinder(h=ht2-1,d=2);
	}
}

module mainpulley() {
	difference(){
		beltwheel(2*ceil(PI*(Ssize+28)/4),Ssize+2.5);
		for(i=[0:1:3])		// holes for yarn post
			rotate([0,0,i*asin(62/Ssize)])translate([hSsize+9,0,-1]) cylinder(h=10, d=2.5);
	}
}

module beltwheel(teeth,bearing){
od=(2*teeth/PI-1);//outer teeth diameter

	translate([0,0,4.5])
		rotate_extrude(angle=360, convexity = 10, $fn=prace)
			translate([bearing/2,0])
				difference(){
					polygon(points=[[1.125,-4.5],[1.125,4.5],
						[(od-bearing+1.5)/2,4.5],[(od-bearing)/2+0.3,3.7],
						[(od-bearing)/2-1,3.7],[(od-bearing)/2-1,-3.7],
						[(od-bearing)/2+0.3,-3.7],[(od-bearing+1.5)/2,-4.5]]);
					circle(d=4.5);
				}
	linear_extrude(9, convexity = 10){
		difference(){
			for(i=[0:360/teeth:360])
				rotate([0,0,i]) translate([-0.4,0])square([0.8,od/2]);
			circle(d=od-3);
		}
	}
}

module base(){
	difference(){
		union(){		// general body
			rotate_extrude(angle=360,$fn=prace)
				difference(){
					translate([hSsize-28,0])square([8.875,12]);
					translate([hSsize-18,7.5])circle(d=4.5);
				}
			for(i=[0:360/6:359])		// mount points for central cylinder
				rotate([0,0,i]) translate([hSsize-26,0,0]) cylinder(h=12,d=8);
		}
		for(i=[0:360/6:359])
			rotate([0,0,i])
				translate([hSsize-26,0,-1]){
					cylinder(h=14,d=3.5);		// mounting holes
					cylinder(h=4,d=6.5);		// recess for screw head
				}
	}
	linear_extrude(2.5){
		difference(){
			offset(-15) offset(15) 
				union(){
					circle(d=Ssize+10, $fn=6);
					for(i=[0:360/6:359])
						rotate([0,0,i])
							translate([hSsize+10,0])hull(){
								translate([10,0])circle(d=20);
								translate([-10,0])circle(d=30);
							}
				}
			circle(d=Ssize-41);
			for(i=[0:360/6:359])
				rotate([0,0,i])
					translate([hSsize+20,0])circle(d=4);		// mounting holes
		}
	}
}

module baseOLD(){
	difference(){
		union(){		// general body
			rotate_extrude(angle=360,$fn=prace)
				difference(){
					translate([hSsize-26,0])square([56,12]);
					translate([hSsize-18,7.5])circle(d=4.5);
					translate([hSsize-18-1.125,2.5])square([60,9.5]);
				}
			for(i=[0:360/6:359])		// mount points for central cylinder
				rotate([0,0,i]) translate([hSsize-26,0,0]) cylinder(h=12,d=8);
		}
		for(i=[0:360/6:359]){
			rotate([0,0,i])
				translate([hSsize-26,0,-1]){
					cylinder(h=14,d=3.5);		// mounting holes
					cylinder(h=4,d=6.5);		// recess for screw head
					translate([56,0,-1])scale([140/Ssize,1,1])cylinder(h=4.5,d=Ssize/1.75);		// cutouts
				}
			rotate([0,0,i+30]){
				translate([hSsize+22,-1])cylinder(h=6,d=4);		// mounting holes
				translate([hSsize-5,-1])cylinder(h=6,d=18);		// cutouts
			}
		}
	}
}

module beltwheelOLD(teeth) {
	linear_extrude(9){
		circle(d=((teeth*2)/PI)-2.5);
		for(i=[0:360/teeth:360])
			rotate([0,0,i]) translate([-0.4,0])square([0.8,(teeth/PI)-0.5]);
	}
	cylinder(h=0.8, d=((teeth*2)/PI)+0.5);
	translate([0,0,8.2])cylinder(h=0.8, d=((teeth*2)/PI)+0.5);
}


//// section yarnguide

module yarnbase() {
	difference(){
		union(){
			hull(){		// mounting plate
				rotate([0,0,-asin(31/Ssize)])translate([hSsize+9,0,0]) cylinder(h=4, d=10);
				rotate([0,0,asin(31/Ssize)])translate([hSsize+9,0,0]) cylinder(h=4, d=10);
			}
			translate([hSsize+1,-4,0])cube([12,8,12]);		// bunper stop
			translate([hSsize+12,0,0])hull(){		// post holder
				translate([0,+6,0])cylinder(h=30,d=10);
				translate([0,-6,0])cylinder(h=30,d=10);
			}
		}
		rotate([0,0,-asin(31/Ssize)])translate([hSsize+9,0,-1]) cylinder(h=10, d=3.5);		// mount holes
		rotate([0,0,asin(31/Ssize)])translate([hSsize+9,0,-1]) cylinder(h=10, d=3.5);
		translate([hSsize+14,0,0])
			hull(){		// post recess
				translate([0,+4,-1])cylinder(h=32,d=6.5);
				translate([0,-4,-1])cylinder(h=32,d=6.5);
			}
			translate([hSsize-1,0,16])rotate([0,90,0])cylinder(h=20,d=2.5);		// screw hole
	}
}

module yarnpost() {
	translate([hSsize+14,0,0])difference(){
		union(){
			translate([0,0,0])
				hull(){		// stem
					translate([0,+4,0])cylinder(h=92,d=6);
					translate([0,-4,0])cylinder(h=92,d=6);
				}
			translate([-17,0,103])rotate([90,0,90])
				hull(){		// top
					translate([5,-9.5,0])cylinder(h=20,d=8);
					translate([-5,-9.5,0])cylinder(h=20,d=8);
				}
			}
		translate([-18,0,102])rotate([90,0,90])
			hull(){		// top resess
				translate([3,-7,0])cylinder(h=22,d=5.2);
				translate([-3,-7,0])cylinder(h=22,d=5.2);
			}
		translate([-8,0,88])cylinder(h=10,d=2.5);		// screw hole
		translate([-4,0,15])rotate([0,90,0])
			hull(){		// lower slot
				translate([15,0,0])cylinder(h=10,d=4);
				translate([-5,0,0])cylinder(h=10,d=4);
			}
	}
}

module yarnguide(){
	translate([5,0,90]){
		intersection(){		// front plate
			translate([hSsize-28,0,25])rotate([0,90,0])cylinder(h=20,d=50);
			translate([hSsize-28,0,-27])rotate([0,90,0])cylinder(h=20,d=90);
			difference(){
				cylinder(h=25,d=Ssize-34);
				translate([0,0,-1])cylinder(h=27,d=Ssize-36);
				translate([hSsize-33,00,12])rotate([0,90,0])cylinder(h=20,d=3);		// yarn hole
				translate([hSsize-23,-0.5,12])cube([10,1,10]);		// yarn slot
				translate([hSsize-23,-15,-7.5])cube([10,30,10]);
			}
		}
	}
	translate([hSsize-13,0,102])rotate([90,0,90]){
		difference(){
			hull(){		// stem
				translate([3,-7,0])cylinder(h=36,d=5);
				translate([-3,-7,0])cylinder(h=36,d=5);
			}
		translate([0,-10,22])rotate([0,90,90])
			hull(){		// screw slot
				translate([5,0,0])cylinder(h=7,d=3.5);
				translate([-5,0,0])cylinder(h=7,d=3.5);
			}
				translate([-2.5,-3,34])rotate([90,0,0])cylinder(h=7,d=1);		// holes for piano
				translate([2.5,-3,34])rotate([90,0,0])cylinder(h=7,d=1);		//  wire guide
		}
	}
}


//// section crank drive

module drivepulley() {
	difference(){
		union(){
			beltwheel(ceil(PI*(Ssize+28)/4),Ssize/2.3);
			for(i=[0:360/3:359]) 
				rotate([0,0,i])translate([(Ssize/4)+1.5,0,8]) cylinder(d=8,h=3);
		}
		for(i=[0:360/3:359]) 
			rotate([0,0,i])translate([(Ssize/4)+1.5,0,-1]) cylinder(d=2.5,h=14);
	}
}

module drivebase() {
	difference(){
		rotate_extrude(angle=360, $fn=prace){
			translate([(Ssize/4.6)-22.5,0])square([21.25,2]);
			difference(){
				translate([(Ssize/4.6)-7.375,0])square([6.25,12]);
				translate([(Ssize/4.6),7.5])circle(d=4.5);
			}
		}
		translate([(-Ssize/4.6)+15,0,-1]){
			cylinder(d=4.5,h=14);
			for(i=[-5:1:5]){
				rotate([0,0,30+i])translate([((Ssize/2.3)-30)*0.866,0,-1])cylinder(d=4.5,h=14);
				rotate([0,0,-30+i])translate([((Ssize/2.3)-30)*.866,0,-1])cylinder(d=4.5,h=14);
			}
		}
	}
}

module handcrank(){
	difference(){
		union(){
			translate([0,-7.5,0]) cube([Ssize/2.5,15,4]);
			hull()
				for(i=[0:360/3:359])
					rotate([0,0,i]) translate([(Ssize/4)+1.5,0,0]) cylinder(h=4,d=12);
				translate([Ssize/2.5,0,0]) cylinder(d=15,h=6);
			}
		for(i=[0:360/3:359]) 
			rotate([0,0,i])translate([(Ssize/4)+1.5,0,-1]) cylinder(d=3.5,12);	// M3
			translate([0,0,-1])cylinder(d=Ssize/5,10);
			translate([Ssize/2.5,0,-1]) cylinder(d=3.4,10);	// M4
	}
}

module handle(){
	translate([Ssize/2.5,0,0])difference(){
		union(){
			translate([0,0,12])sphere(d=25);
			cylinder(h=15,d=15);
		}
		translate([0,0,-1])cylinder(h=30,d=5.5);
		translate([0,0,17])cylinder(h=10,d=9.5);
	}
}


//// section yarn brake / heel spring
 
module bar(){
	difference(){
		translate([-17,0,0])union(){
			rotate([0,90,0])hull(){		// body
				translate([0,5,0])cylinder(h=72,d=8);
				translate([0,-5,0])cylinder(h=72,d=8);
			}
		translate([52,9,0])rotate([90,0,0])cylinder(h=18,d=8);		// lock pivot
		translate([0,9,0])rotate([90,0,0])cylinder(h=18,d=8);		// lever pivot
		}
		translate([35,13,0])rotate([90,0,0])cylinder(h=26,d=3.2);		// lock pivot
		translate([-17,13,0])rotate([90,0,0])cylinder(h=26,d=3);		// lever pivot
		translate([0,0,-5])cylinder(h=10,d=6.1);		// mounting hole
		translate([0,13,0])rotate([90,0,0])cylinder(h=26,d=1.5);		// locking pin
		hull(){		// lever cutout
			translate([-27,-5,-5])cube([10,10,10]);
			translate([-12,0,-5])cylinder(h=10,d=10);
		}
		translate([44.5,-2.5,-5])cylinder(h=12,d=1);		// locking guide
		translate([44.5,2.5,-5])cylinder(h=12,d=1);
		translate([45,6,0])rotate([0,90,0])cylinder(h=12,d=1);		// front wire guide
		translate([45,-6,0])rotate([0,90,0])cylinder(h=12,d=1);
		translate([35,0,-6])rotate([0,-70,-8])cylinder(h=40,d=1);		// rear wire guide
	}
}

module brake(){
	difference(){
	translate([0,11,0])rotate([90,0,0])difference(){
		union(){
			hull(){
				translate([35,-1,0])cylinder(h=2,d=5);
				translate([14,3.5,0])cylinder(h=2,d=6);
				translate([0,0,0])cylinder(h=2,d=7);
			}
			translate([0,0,20])hull(){
				translate([35,-1,0])cylinder(h=2,d=5);
				translate([14,3.5,0])cylinder(h=2,d=6);
				translate([0,0,0])cylinder(h=2,d=7);
			}
			translate([35,-1,0])cylinder(h=20,d=5);
		}
		translate([14,3.5,-1])rotate([0,0,0])cylinder(h=24,d=3);
		translate([0,0,-1])rotate([0,0,0])cylinder(h=24,d=3);
	}
		translate([35,-3,-4.5])cylinder(h=7,d=1);
		translate([35,3,-4.5])cylinder(h=7,d=1);
	}
}

module lever() {
		rotate([90,0,0])difference(){
			union(){
				hull(){
					translate([0,0,3.5])cylinder(h=2, d=8);
					translate([-20,0,3.5])cylinder(h=2, d=6);
				}
				hull(){
					rotate([90,0,-40])translate([-10,3,-10])cylinder(h=12,d=5);
					translate([0,0,0.5])cylinder(h=5,d=8);
				}
				translate([0,0,-3.5])cylinder(h=9,d=8);
			}
			translate([0,0,-5])cylinder(h=15,d=3.2);
			translate([-10,0,2])cylinder(h=4,d=1.5);
			translate([-15,0,2])cylinder(h=4,d=1.5);
			translate([-20,0,2])cylinder(h=4,d=1.5);
			rotate([90,0,-40])translate([-10,3,-11])cylinder(h=14,d=1);
	}
}

module weight(){
	difference(){
		union(){
			cylinder(h=18,d=10);
			hull(){
				cylinder(h=6,d=10);
				translate([-32.2,0,0])cylinder(h=6,d=6);
			}
			translate([-32,0,0])rotate([90,0,0])hull(){
				translate([0,9,-1])cylinder(h=2,d=6);
				translate([-3,0,-1])cube([6,6,2]);
			}
		}
		
		translate([0,0,-1])cylinder(h=20,d=6.5);
		translate([-32,0,-1])cylinder(h=8,d=2);
		translate([-32,-2,9])rotate([-90,0,0])cylinder(h=4,d=1.5);
		
	}
}

module brakebase(){
	difference(){
		union(){
			cylinder(h=20,d=12);
			hull(){
				translate([-8,-14.5,0])cylinder(h=3,d=8);
				translate([8,-14.5,0])cylinder(h=3,d=8);
				translate([-8,14.5,0])cylinder(h=3,d=8);
				translate([8,14.5,0])cylinder(h=3,d=8);
			}
			translate([0,0,-15]){
				rotate([45,0,38])	translate([-1.5,-0,-0])cube([3,25,25]);
				rotate([45,0,-38])	translate([-1.5,-0,-0])cube([3,25,25]);
			}
		}
		translate([0,0,-1])cylinder(h=22,d=6.1);
		translate([0,-14,-1])cylinder(h=8,d=4.2);
		translate([0,14,-1])cylinder(h=8,d=4.2);
		translate([-7,0,14])rotate([0,90,0])cylinder(h=14,d=1.5);
		translate([0,0,-30])cylinder(h=30,d=50);
	}
}


////section common

module ballcage(bsize) {
	balls=360/floor(PI*bsize/10);
	echo("number of balls:",360/balls);
	difference(){
		cylinder(h=6, d=bsize+1.2);
		translate([0,0,-2])cylinder(h=10, d=bsize-1.2);
		for(i=[0:balls:359]){  
			rotate([0,0,i]) translate([0,0,4])rotate([90,0,0]) cylinder(h=bsize+10,d=5); 
		} 
	}
}

module nut(){
	if (metric==true) 	// M3 
		cylinder(h=3,d=6.35,$fn=6);
	else	// #4 UNC
		cylinder(h=3,d=7.35,$fn=6);
}

//// section tools (WIP)

module basket(){
	difference(){
		cylinder(h=6,d=80);
		translate([0,0,2])cylinder(h=5,d=76);
		for(i=[0:720/n:360])
			rotate([0,0,i])translate([36,0,-1])cylinder(h=4,d=3);
	}
	difference(){
		cylinder(h=12,d=12);
		translate([0,0,-1])cylinder(h=14,d=3.2);
	}
}
module magnet(r){
	difference(){
		translate([hSsize-1,0,7])rotate([0,90,0]){
			hull(){
				translate([0,-3,0])cylinder(h=r-2.5,d=5);
				translate([0,3,0])cylinder(h=r-2.5,d=5);
				translate([0,-3,r-2.5])sphere(d=5);
				translate([0,3,r-2.5])sphere(d=5);
			}
			hull(){
				translate([0,-3,0])cylinder(h=3,d=5);
				translate([0,3,0])cylinder(h=3,d=5);
				translate([7,0,0])cylinder(h=3,d=8);
			}
		}
		translate([0,0,-5])cylinder(h=20,d=Ssize);
		translate([hSsize-4,0,0])rotate([0,90,0])cylinder(h=10,d=3.5);
		translate([hSsize-3+r,3.25,7])rotate([90,0,0])
		hull(){
			cylinder(h=6.5,d=4);
			translate([2,0,0])cylinder(h=6.5,d=4);
		}
	}
}

module display(){
	translate([13,-6,0]){
		difference(){
			union(){
				cube([46,13,32]);
				translate([-3,6,16])rotate([0,90,0])cylinder(h=3,d=12);
				}
			translate([4,-1,5])cube([30,35,22]);
			translate([1,1,1])cube([44,15,30]);
			translate([41,-1,16])rotate([-90,0,0])cylinder(h=12,d=4);
			translate([-4,6,16])rotate([0,90,0])cylinder(h=7,d=3);
			translate([6,7,-1])cube([6,3,10]);
		}
		translate([70,0,0]){
			difference(){
				union(){
					cube([46,1,32]);
					translate([1.1,0,1.1])cube([43.8,3,29.8]);
				}
				translate([0,1,10])cube([46,3,12]);
				translate([6,1,24])cube([8,3,10]);
			}
		}
	}
}

module display1(){
	translate([13,-6,0]){
		difference(){
			union(){
				cube([44,13,32]);
				translate([-3,6,16])rotate([0,90,0])cylinder(h=3,d=12);
				}
			translate([1,1,1])cube([42,15,30]);
			translate([11,-1,9])cube([22,35,14]);
			translate([41,-1,16])rotate([-90,0,0])cylinder(h=12,d=4);
			translate([-4,6,16])rotate([0,90,0])cylinder(h=7,d=3);
			translate([6,7,-1])cube([6,3,10]);
		}
		translate([4,1,12]) pillar();
		translate([4,1,28]) pillar();
		translate([40,1,12]) pillar();
		translate([40,1,28]) pillar();
		
		translate([70,0,0]){
			difference(){
				union(){
					cube([44,1,32]);
					translate([1.1,0,1.1])cube([41.8,3,29.8]);
				}
				translate([2,1,2])cube([40,3,28]);
				translate([6,1,24])cube([8,3,10]);
			}
		}
	}
	module pillar(){
		rotate([-90,0,0]){
			difference(){
				cylinder(h=6.2,d=6);
				cylinder(h=9,d=2.5);
			}
		}
	}
}

module displaymount(){
	translate([13,-6,0])
	difference(){
		hull(){
			translate([-6,6,16])rotate([0,90,0])cylinder(h=1,d=12);
			translate([-13,6,10])cylinder(h=12,d=10);
		}
		translate([-13,6,-1])cylinder(h=34,d=6);
		translate([-14,6,16])rotate([0,90,0])cylinder(h=10,d=3);
		translate([-13.5,6,16])rotate([-90,0,0])cylinder(h=6,d=2.5);
	}
}
		
module reedsensor(){
	difference(){
		hull(){
			translate([0,0,4])rotate([0,90,0])cylinder(h=13,d=8);
			translate([13,9,4])rotate([90,0,0])cylinder(h=18,d=8);
			translate([0,0,-0])cylinder(h=10,d=10);
		}
		translate([0,0,-1])cylinder(h=12,d=6);
		hull(){
			translate([16,8,4])rotate([90,0,0])cylinder(h=16,d=3);
			translate([13,8,4])rotate([90,0,0])cylinder(h=16,d=2);
		}
		translate([6,0,3])cylinder(h=12,d=2);
		translate([1,0,4])rotate([0,90,0])cylinder(h=14,d=4);
		translate([-10,0,4])rotate([0,90,0])cylinder(h=20,d=2.5);
	}
}
