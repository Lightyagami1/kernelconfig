# Copyright 1999-2015 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Id$

EAPI=6

DESCRIPTION="A classical example to use when starting on something new"
HOMEPAGE="https://github.com/Lightyagami1/kernelconfig"
SRC_URI="https://github.com/Lightyagami1/kernelconfig"

LICENSE="MIT"
SLOT="0"
KEYWORDS="~amd64 ~x86"


RDEPEND = ">=dev-lang/python-3"


src_configure() {
    econf --with-posix-regex
}

src_install() {
    emake DESTDIR="${D}" install
    
    dodoc FAQ NEWS README
    dohtml README.html
}
