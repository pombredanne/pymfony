# -*- coding: utf-8 -*-
# This file is part of the pymfony package.
#
# (c) Alexandre Quercia <alquerci@email.com>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.

from __future__ import absolute_import;

from pymfony.component.kernel.bundle import Bundle;

from pymfony.component.dependency import ContainerBuilder;
from pymfony.component.dependency import Scope;
from pymfony.component.dependency.compiler import PassConfig;

from pymfony.bundle.framework_bundle.dependency.compiler import RegisterKernelListenersPass;
from pymfony.bundle.framework_bundle.dependency.compiler import AddCacheWarmerPass;
from pymfony.bundle.framework_bundle.dependency.compiler import AddCacheClearerPass;
from pymfony.bundle.framework_bundle.dependency.compiler import CompilerDebugDumpPass;
from pymfony.bundle.framework_bundle.dependency.compiler import RoutingResolverPass;

"""
Pymfony FrameworkBundle
"""

class FrameworkBundle(Bundle):
    """Bundle.

    @author: Fabien Potencier <fabien@symfony.com>

    """

    def build(self, container):
        assert isinstance(container, ContainerBuilder);

        Bundle.build(self, container);

        container.addScope(Scope('request'));

        container.addCompilerPass(RoutingResolverPass());
        container.addCompilerPass(RegisterKernelListenersPass(), PassConfig.TYPE_AFTER_REMOVING);
        container.addCompilerPass(AddCacheWarmerPass());
        container.addCompilerPass(AddCacheClearerPass());

        if container.getParameter('kernel.debug') :
            container.addCompilerPass(CompilerDebugDumpPass(), PassConfig.TYPE_AFTER_REMOVING);
