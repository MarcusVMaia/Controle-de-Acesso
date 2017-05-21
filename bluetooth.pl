#!/usr/bin/perl

use Net::Bluetooth;

my $device_ref = get_remote_devices();
my $filename = "MACBTLIST.json";
my @MACS;
my @NAME;
my $INIC, $DEVICE, $MIDDLE, $JSON, $FIM;
my $controle1;
my $controle2;
my $contador = 0;

$INIC = <<'END_INIC';
{
"deviceList":[
END_INIC

$FIM = <<'END_FIM';
]}
END_FIM

foreach $addr (keys %$device_ref) {
	$controle1++;
	push @MACS, $addr;
	push @NAME, $device_ref->{$addr};
}

foreach (@MACS){
$controle2++;
if($controle2 == $controle1){
	$DEVICE = <<"END_DEVICE";
	{
	 "deviceName:"$NAME[$contador]",
	 "MAC:"$MACS[$contador]"
	}
END_DEVICE
}else{
$DEVICE = <<"END_DEVICE";
	{
	 "deviceName:"$NAME[$contador]",
	 "MAC:"$MACS[$contador]"
	},
END_DEVICE
}
$contador++;
$MIDDLE .= $DEVICE;
}

$JSON = join "", $INIC, $MIDDLE, $FIM;

open(my $fh,">",$filename);
print $JSON;
print $fh $JSON;
close $fh;
