#!/usr/bin/perl --

#########################################
#
# web���著�MCGI
#
# ��E����ł�
#
#########################################

# ����CGI�̃t�@�C����
$base = "./clap.cgi";

#----------�O���t�@�C���ǂݍ��݁i�T�[�o�[�ɂ���Ă͐�΃p�X�Ŏw��j
require './jcode.pl';
require './clapinit.cgi';

#---------�t�H�[���f�R�[�h
&decode;


#########################################

#---------���O�̓ǂݍ��݁A���Z�A�ۑ�

&lockon;             #���b�N�J�n

open(IN,"$logfile");  #===========���O�t�@�C������ǂݍ���
@logdata = <IN>;
close(IN);

#---------���O�̕���
($logdate,$logtotal,$log[0],$log[1],$log[2],$log[3],$log[4],$log[5],$log[6],$log[7],$log[8],$log[9],$log[10],$log[11],$log[12]
     ,$log[13],$log[14],$log[15],$log[16],$log[17],$log[18],$log[19],$log[20],$log[21],$log[22],$log[23])
              = split( /<>/ , $logdata[$#logdata] );

#---------���t�擾
$day = 0;
&dateload;

#---------���t�`�F�b�N
if ($getdate ne $logdate){

#---------���t�ύX���A�[�����O�ǉ��A�ߋ����O�폜
 @log = (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
 $logtotal = 0;
 @logdata = (@logdata,"\n");

 $data = "$getdate<>";

 $data = "$data$logtotal<>";

 for ($i=0 ; $i<=23 ; $i++){
  $data = "$data$log[$i]<>";
 }

 $logdata[$#logata] = "$data\n";


 $day = 14;
 & dateload; 

 $j = $#logdata;
 for ( $i=0 ; $i<=$j ; $i++ ){

  ($logdate,$xxx) = split(/<>/,$logdata[0]);
  if ($logdate < $getdate){shift (@logdata);}

 }

#---------���t�ύX���A�ߋ����O���b�Z�[�W�폜
 open(IN,"$mesfile");
 @mesdata = <IN>;
 close(IN);

 $j = $#mesdata;
 for ( $i=0 ; $i<=$j ; $i++ ){

  ($logdate,$xxx) = split(/<>/,$mesdata[0]);
  if ($logdate < $getdate){shift (@mesdata);}

 }

 open(OUT,">$mesfile");
 print OUT @mesdata;
 close(OUT);

}

#---------���O���Z
$log[$tohour] ++;
$logtotal ++;

#---------�ۑ��p���O�쐬
$day = 0;
& dateload;


$data = "$getdate<>";

$data = "$data$logtotal<>";

for ($i=0 ; $i<=23 ; $i++){
 $data = "$data$log[$i]<>";
}

$logdata[$#logata] = "$data\n";

#---------���O�㏑���ۑ�
open(OUT,">$logfile");
print OUT @logdata;
close(OUT);

#---------------------------------------�ꌾ���b�Z�[�W����
if ($hitokoto ne ''){

$mesdata = "$getdate<>$tohour<>$hitokoto<>\n";

open(OUT,">>$mesfile");
print OUT $mesdata;
close(OUT);

}


&lockoff;          #���b�N�I��


#-----------------------------------�g�s�l�k�\��
$title = "web���著�M����";

&header;

print "<body class=clap>\n";

#------���b�Z�[�W
$i = int(rand(4));

print "<center>\n";

print "$message[$i]<br><br><br>\n";

#====================����ɑ���t�H�[�������b�Z�[�W

if ($kaisuu < 9){

 $kaisuu ++;

 print "<FORM action=$base method=POST>\n";
 print '<INPUT class="clap" type="submit" value="�����Ƒ���"><br><br>',"\n";
 print "<input type=hidden name=kaisuu value=$kaisuu>\n";
 print '�����ꌾ����΁A�ǂ����B<br>',"\n";
 print '<input class=nor type=text name=hitokoto size=50 maxlength=200><br>',"\n";
 print '</FORM>',"\n";

}else{

 print '<font size=2>��������h�~�̂��߁A10��ȏ�A���Ŕ���𑗂�Ȃ��悤�ɂȂ��Ă��܂��B</font>';

}

print "<br>\n";


#---------------------���쌠�\���Aweb��������T�C�g�ւ̃����N�i�폜�s�j
print '<a href="http://www.webclap.com/" target="_blank">*web����CGI�����T�C�g*</font></a><br>',"\n";



print "</center>\n";
print "</body></html>\n";

exit;
