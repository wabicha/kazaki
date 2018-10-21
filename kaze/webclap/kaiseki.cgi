#!/usr/bin/perl --

#########################################
#
# web������CGI
#
# ��E����ł�
#
#########################################

# ����CGI�̃t�@�C����
$base = "kaiseki.cgi";

#----------�O���t�@�C���ǂݍ��݁i�T�[�o�[�ɂ���Ă͐�΃p�X�Ŏw��j
require 'jcode.pl';
require 'clapinit.cgi';

#----------�p�����[�^���擾
$pal = $ENV{'QUERY_STRING'};
($pass,$logday) = split(/&/,$pal);


#----------�p�����[�^�̓��t���������Ȃ����`�F�b�N
if ($logday > 13) {$logday = 0;}
if ($logday eq '') {$logday = 0;}


#----------�h�c�A�p�X���[�h�A��͌��J�F��
&passcheck;

#---------���O�̓��t���`�F�b�N
&logdate;

#----------���O�쐬���̓��ɂ��擾
$day = $logday;
&dateload;


#---------��͗p�f�[�^���o
& makelog;
& makemes;

#---------���O�̍ō��l���o
$logmax = 0;
for ($i=0 ; $i<=23 ; $i++){

 if ($logmax < $log[$i]){ $logmax = $log[$i]; }

}

#---------�ߋ�14�����̃g�[�^�����o
@pasttotal = (0,0,0,0,0,0,0,0,0,0,0,0,0,0);
($pastdate,$pasttotal[0]) = split(/<>/,$logs[$#logs]);
$pastmax = $pasttotal[0];

for ($i=1 ; $i<=13 ; $i++){

 $day=$i;
 &dateload;

 for ($l=0 ; $l<=$#logs ; $l++){

  ($pastdate,$pasttotal) = split(/<>/,$logs[$l]);
  if ($getdate eq $pastdate){ $pasttotal[$i]=$pasttotal; }

 }

 if ($pastmax < $pasttotal[$i]){$pastmax = $pasttotal[$i];}

}


$day = $logday;
&dateload;
#----------------------HTML�\��
$title = "web������";
&header;

print '<body>';
print "<center>\n";

print "$tomon��$today����web������<br><br>\n";


#-----------��͌��ʕ\��

print "<table border>\n";

print "<td><center>����</center></td><td><center>���l</center></td>\n";
print "<td><center>�O���t</center></td><tr>\n";

for ($i=0 ; $i<=23 ; $i++){

 print '<td><font size=2><p align="right">',"$i��</p></font></td>\n";
 print '<td><font size=2><p align="right">',"$log[$i]</p></font></td>\n\n";

  if ($logmax){
   $graph = $log[$i] / $logmax * 400;
   print "<td><IMG src=\"$graph1\" width=\"$graph\" height=\"10\" border=\"0\"></td>";
  }
   else {
    print "<td><IMG src=\"$graph1\" width=\"0\" height=\"10\" border=\"0\"></td>";
   }

 print "<tr>\n";
}

print "<td><center>���v</center></td>";
print "<td><p align=\"right\">$logtotal</p></td>";
print "<td width=\"400\">�@</td>";

print "</table><br>\n";

#----------------------���b�Z�[�W�\��
print "��������ꂽ���b�Z�[�W<br>\n";
print "<table border>\n";

for ($i=0 ; $i<=$#mes ; $i++){

 ($mesday,$meshour,$message) = split(/<>/,$mes[$i]);

 print "<td><p align=\"right\">$meshour��</p></td>\n";
 print "<td>$message</td><tr>\n\n";

 $sousinmessage = "$sousinmessage\n$message";

}

print "</table><br>\n";

#---------------------�ߋ�2�T�Ԃ̃O���t�ƕʂ̓��ւ̃����N
print "�ߋ�14���Ԃ̉��<br>";
print "<table border>\n";

#---------------�O���t
for ($i=0 ; $i<=13 ; $i++){

  if ($pastmax){
   $graph = $pasttotal[$i] / $pastmax * 200;
   print "<td height=200 valign=bottom align=center><IMG src=\"$graph2\" width=\"20\" height=\"$graph\" border=\"0\"></td>\n";
  }
   else {
    print "<td height=200 valign=bottom align=center><IMG src=\"$graph2\" width=\"20\" height=\"0\" border=\"0\"></td>\n";
   }
}

#--------------���l
print "<tr>\n";

for ($i=0 ; $i<=13 ; $i++){

 print "<td><center><font size=2>$pasttotal[$i]</font></center></td>\n"

}

#-------------���ɂ��ƃ����N
print "<tr>\n";

for ($i=0 ; $i<=13 ; $i++){

 $day=$i;
 &dateload;

 print "<td><center><font size=2><a href=\"$base?$pass&$i\">$tomon��$today��</a></font></center></td>\n";

}

print "</table><br><br>\n";

#------------------���쌠�\���A�����T�C�g�ւ̃����N�i�폜�s�j

print "<br>\n";
print '<a href="http://www.webclap.com/" target="_blank"><font size=2>web����CGI�����T�C�g</font></a><br><br><br>',"\n";




print "</center>";
print "</body></html>\n";

exit;





#---------���O���o
sub makelog{

#----------���O�I�[�v��
&lockon;          #====���b�N�J�n

open(IN,"$logfile");
@logs = <IN>;
close(IN);

&lockoff;       #=================���b�N�I��


 for ($i=0 ; $i <= $#logs ; $i++){

  ($logdate,$logtotal,$log[0],$log[1],$log[2],$log[3],$log[4],$log[5],$log[6],$log[7],$log[8],$log[9],$log[10],$log[11],$log[12]
     ,$log[13],$log[14],$log[15],$log[16],$log[17],$log[18],$log[19],$log[20],$log[21],$log[22],$log[23])
              = split(/<>/,$logs[$i]);

  if ($logdate eq $getdate) { return; }

 }

 $logdate = $getdate;
 @log = (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
 $logtotal = 0;

}

#---------------���b�Z�[�W���o
sub makemes{

 &lockon;  #====���b�N�J�n

 open(IN,"$mesfile");  #===========�ߋ����b�Z�[�W����ǂݍ���
 @mesdata = <IN>;
 close(IN);

 &lockoff;  #=================���b�N�I��

 for ($i=0 ; $i <= $#mesdata ; $i++){

  ($mesday,$meshour,$message) = split(/<>/,$mesdata[$i]);

  if ($mesday eq $getdate) { @mes = (@mes,$mesdata[$i]); }

 }

}

#--------------�p�X���[�h�F��
sub passcheck{

if ($passlock eq 0){ return; }

if ($pass eq $password){ return; }

$title = '�p�X���[�h�F�؃G���[';

&header;

print "<body>\n";
print "<center>\n";
print '�p�X���[�h���Ⴂ�܂�<br><br>';
print '��������͂�\��������ɂ́A<br>��͂b�f�h�̂t�q�k�̌�� "?�p�X���[�h" ��ǉ����Ă��������B<br>';
print '<br>��F�p�X���[�h��"0123"�������ꍇ<br><br>';
print "http://�`�`�`/$base?0123";
print '<br><br>�ƂȂ�܂��B';
print "</center>\n</body></html>";

exit;
}


#-------------------���O�̓��t�`�F�b�N
sub logdate{

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


&lockoff;          #���b�N�I��

}