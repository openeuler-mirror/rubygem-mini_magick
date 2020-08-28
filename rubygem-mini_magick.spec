%global gem_name mini_magick
Name:                rubygem-%{gem_name}
Version:             4.8.0
Release:             1
Summary:             Manipulate images with minimal use of memory via ImageMagick
License:             MIT
URL:                 https://github.com/minimagick/minimagick
Source0:             https://rubygems.org/gems/%{gem_name}-%{version}.gem
Source1:             https://github.com/minimagick/minimagick/archive/v%{version}.tar.gz
Patch0:              mini_magick-4.8.0-Use-smallcase-for-Image-details-in-tests.patch
Patch1:              mini_magick-4.8.0-match-new-identify-error-message-in-tests.patch
Requires:            ImageMagick
BuildRequires:       ruby(release) rubygems-devel ruby rubygem(rspec) rubygem(webmock) ImageMagick
BuildArch:           noarch
%description
A ruby wrapper for ImageMagick command line. Using MiniMagick the ruby
processes memory remains small (it spawns ImageMagick's command line program
mogrify which takes up some memory as well, but is much smaller compared
to RMagick).

%package doc
Summary:             Documentation for %{name}
Requires:            %{name} = %{version}-%{release}
BuildArch:           noarch
%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version}
ln -s minimagick-%{version}/spec spec

%build
gem build ../%{gem_name}-%{version}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
tar xzvf %{SOURCE1}
cat %{PATCH0} | patch -p1
cat %{PATCH1} | patch -p1
sed -i -e '/require "pry"/ s/^/#/g' \
       -e '/require "bundler/ s/^/#/g' \
  spec/spec_helper.rb
sed -i -e '/^  \[:imagemagick, :graphicsmagick\].each do |cli|$/ s/, :graphicsmagick//g' \
       -e '/^  \["open3", "posix-spawn"\].each do |shell_api|$/ s/, "posix-spawn"//g' \
  spec/spec_helper.rb
sed -i '/^    it "identifies when gm exists" do$/,/    end/ s/^/#/g' \
  spec/lib/mini_magick/utilities_spec.rb
sed -i "/^    it \"returns GraphicsMagick's version\" do$/,/    end/ s/^/#/g" \
  spec/lib/mini_magick_spec.rb
rspec spec
popd

%files
%dir %{gem_instdir}
%license %{gem_instdir}/MIT-LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%{gem_instdir}/Rakefile

%changelog
* Wed Aug 19 2020 geyanan <geyanan2@huawei.com> - 4.8.0-1
- package init
