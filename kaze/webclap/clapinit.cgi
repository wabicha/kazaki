######################################################
#
#
#  web����CGI��{�ݒ聕��v�T�u���[�`��
#
#
######################################################

#-----------
# ��{�ݒ�
#-----------


# ��͂Ƀp�X���[�h�F�؂�
# 0�c�����Ȃ�
# 1�c������
$passlock = '0';

# ��͉{���p�p�X���[�h�i�p�X���[�h�F�؂������Ȃ��ꍇ�͕s�v�j
$password = '0000';

# ���著�M���ʗp���烁�b�Z�[�W1�i�^�O�g�p�j
$message[0]='���肪���M����܂����B<br>���肪�Ƃ��������܂��B<br><Img src="shed/oebi-01.jpg">';

# ���著�M���ʗp���烁�b�Z�[�W2�i�^�O�g�p�j
$message[1]='���肪���M����܂����B<br>���ӊ��ӁI<br><Img src="shed/oebi-02.jpg">';

# ���著�M���ʗp���烁�b�Z�[�W3�i�^�O�g�p�j
$message[2]='���肪���M����܂����B<br>���ꂩ����ǂ����悵�ȂɁB<br><Img src="shed/oebi-03.jpg">';

# ���著�M���ʗp���烁�b�Z�[�W4�i�^�O�g�p�j
$message[3]='���肪���M����܂����B<br>���肪�Ƃ��������܂��B<br><Img src="shed/oebi-04.jpg">';

# ���著�M���ʗp���烁�b�Z�[�W5�i�^�O�g�p�j
$message[4]='���肪���M����܂����B<br>���肪�Ƃ��������܂��B��݂ɂȂ�܂��B<br><Img src="shed/oebi-04.jpg">';


# ���O�t�@�C��
$logfile = './log.dat';

# �ꌾ���b�Z�[�W�ۑ��t�@�C��
$mesfile = './mes.dat';

# �t�@�C�����b�N��
# 0�c���Ȃ�
# 1�c����
# ���Ȃ�̐��̔��肪�����Ă���Ǝv����ꍇ��1�ɂ��Ă��������B
# �t�@�C�����b�N�ɂ�flock�֐����g�p���܂��B�T�[�o�[�̂n�r�̑Ή��󋵂����m�F��������
$lock = '0';

# ���b�N�t�@�C�����i�t�@�C�����b�N�����Ȃ��ꍇ�͕s�v�j
$lockfile = 'lock.dat';

# �O���tURL(�T�[�o�[�ɂ���Ă͐�΃p�X�j
# cgi�t�H���_�ɉ摜���u���Ȃ��T�[�o�[������̂Œ��ӂ��Ă�������
$graph1 = './graph1.gif';    #��
$graph2 = './graph2.gif';    #�c


#----------
# �ݒ�I��
#----------



#--------------
# HTML�w�b�_�[
#--------------
sub header{

print "Content-type: text/html\n\n";
print '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">',"\n";
print '<html lang="ja"><head>',"\n";
print "<title>$title</title>\n";
print '<link rel="stylesheet" href="../kaze-css.css">',"\n";
print "</head>\n";

}


#----------
# ���t�擾
#----------
sub dateload{

$ENV{'TZ'} = "JST-9";
($sec,$min,$tohour,$today,$tomon,$toyear,$wday,$yday,$isdst) = (localtime(time-$day*86400));

$toyear += 1900;
$tomon ++;

$getdate = "$toyear";

if ($tomon <= 9){ $getdate = "$getdate"."0$tomon"; }
         else { $getdate = "$getdate$tomon"; }

if ($today <= 9){ $getdate = "$getdate"."0$today"; }
         else { $getdate = "$getdate$today"; }

}


#------------------
# �t�H�[���f�R�[�h
#------------------
sub decode {
	local($buf, $key, $val);

	if ($ENV{'REQUEST_METHOD'} eq "POST") {
		read(STDIN, $buf, $ENV{'CONTENT_LENGTH'});
	}
	%in=();
	foreach (split(/&/, $buf)) {
		($key, $val) = split(/=/);
		$val =~ tr/+/ /;
		$val =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

		# S-JIS�R�[�h�ϊ�
		&jcode'convert(*val, "sjis", "", "z");

		# �^�O����
		$val =~ s/&/&amp;/g;
		$val =~ s/"/&quot;/g;
		$val =~ s/</&lt;/g;
		$val =~ s/>/&gt;/g;
		$val =~ s/\0//g;

		# ���s����
		if ($key eq "comment") {
			$val =~ s/\r\n/<br>/g;
			$val =~ s/\r/<br>/g;
			$val =~ s/\n/<br>/g;
		} else {
			$val =~ s/\r//g;
			$val =~ s/\n//g;
		}
		$in{$key} .= "\0" if (defined($in{$key}));
		$in{$key} .= $val;
	}
        $pass = $in{'pass'};
        $hitokoto = $in{'hitokoto'};
        $kaisuu = $in{'kaisuu'};
}


#---------------------
# �t�@�C�����b�N�J�n
#---------------------
sub lockon{

 if ($lock eq '1'){

  open(LOCK,">$lockfile");  #====���b�N�J�n
  flock (LOCK,2);

 }

}

#---------------------
# �t�@�C�����b�N�I��
#---------------------
sub lockoff{

 if ($lock eq '1'){

  unlink( "$lockfile" );
  flock( LOCK, 8 );
  close( LOCK );  #=================���b�N�I��

 }

}
