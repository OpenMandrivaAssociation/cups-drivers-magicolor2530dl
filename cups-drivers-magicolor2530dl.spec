%define rname magicolor2530dl

Summary:	Cups Driver for KONICA MINOLTA magicolor 2530 DL
Name:		cups-drivers-%{rname}
Version:	2.1.1
Release:	20
License:	GPLv2
Group:		System/Printing
Url:		http://printer.konicaminolta.net/
Source0:	magicolor2530DL-%{version}.tar.gz
Patch0:		magicolor2430DL-shared_system_libs.diff
Patch1:		magicolor-automake-1.13.patch

BuildRequires:	cups-devel
BuildRequires:	jbig-devel
BuildRequires:	pkgconfig(lcms)
Requires:	cups

%description
This package contains KONICA MINOLTA CUPS LavaFlow stream(PCL-like) filter
rastertokm2530dl and the PPD file. The filter converts CUPS raster data to
KONICA MINOLTA LavaFlow stream.

This package contains CUPS drivers (PPD) for the following printers:

 o KONICA MINOLTA magicolor 2530 DL printer

%prep
%setup -qn magicolor2530DL-%{version}
%apply_patches

# Fix copy of CUPS headers in kmlf.h
perl -pi -e 's:\bcups_strlcpy:_cups_strlcpy:g' src/kmlf.h

# Remove asterisks from group names in PPD file
gzip -dc src/km_en.ppd.gz | perl -p -e 's/(Group:\s+)\*/$1/g' | gzip > src/km_en.tmp.ppd.gz && mv -f src/km_en.tmp.ppd.gz src/km_en.ppd.gz

# Determine the directory for the CUPS filters using the correct method
perl -pi -e 's:(CUPS_SERVERBIN=)"\$libdir/cups":$1`cups-config --serverbin`:' configure*

rm -f configure
autoreconf -fi

%build
%configure2_5x

%make

%install
%makeinstall_std

%files
%doc AUTHORS COPYING ChangeLog
%{_prefix}/lib/cups/filter/rastertokm2530dl
%{_datadir}/KONICA_MINOLTA/mc2530DL
%{_datadir}/cups/model/KONICA_MINOLTA/km2530dl.ppd*

